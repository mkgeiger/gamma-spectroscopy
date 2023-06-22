#include <SPI.h>
#include "Mcp320x.h"
#include <WiFiManager.h>
#include <ESPmDNS.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include <TimeLib.h>

// access point
#define AP_NAME           "GammaConnectAP"
#define AP_TIMEOUT        60

// GPIOs
#define LED_PIN           17   // 2 for onboard blue LED
#define INT_PIN           22   // event capture
#define RST_PIN           21   // reset sample & hold
#define VSPI_CS_PIN        5   // SPI chip select

// ADC MCP3201-B
#define ADC_BITS          12                 // resolution
#define ADC_CHANNELS      (1ul << ADC_BITS)
#define ADC_VREF          3300               // 3.3V Vref
#define ADC_CLK           800000             // SPI clock 800kHz

// variables
static volatile uint32_t  events = 0ul;
static uint32_t           last_timestamp = 0ul;
static uint16_t           spectrum[ADC_CHANNELS] = {0u};
static uint8_t            led_time = 0u;
static char               timebuf[20];
static double             minutes;
static MCP3201            adc(ADC_VREF, VSPI_CS_PIN);
static WiFiManager        wifiManager;
static AsyncWebServer     server(80);

// WiFi events
void WiFiEvent(WiFiEvent_t event)
{
    Serial.printf("WiFi-event: %d\n", event);

    switch (event)
    {
    case SYSTEM_EVENT_STA_GOT_IP:
        Serial.println("WiFi connected.");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());
        break;
    case SYSTEM_EVENT_STA_DISCONNECTED:
        Serial.println("WiFi lost connection.");
        break;
    default:
        break;
    }
}

// time elapsed since reset
static void timeSinceReset(char *timebuf)
{
    uint32_t seconds = (millis() - last_timestamp) / 1000;
    uint32_t minutes = seconds / 60;
    uint32_t hours = minutes / 60;
    uint32_t days = hours / 24;

    seconds %= 60;
    minutes %= 60;
    hours %= 24;
    sprintf(timebuf, "%02d.%02d:%02d:%02d\0", days, hours, minutes, seconds);
}

// minutes since reset
static float minutesSinceReset(void)
{
    uint32_t seconds = (millis() - last_timestamp) / 1000;
    return ((float)seconds / 60.0);
}

// reset sample and hold circuit
static void resetSampleHold(void)
{
    digitalWrite(RST_PIN, HIGH);
    delayMicroseconds(1);  // discharge for 1 µs, actually takes 2 µs - enough for a discharge
    digitalWrite(RST_PIN, LOW);
}

// event capture ISR
void IRAM_ATTR handleInterrupt(void)
{
    uint16_t raw;

    // turn on LED for at least 100 ms
    digitalWrite(LED_PIN, HIGH);
    led_time = 200u;

    // wait at least 3 µs to allow the sample/hold circuit to stabilize
    delayMicroseconds(3);

    // 1 measurements takes about 25 µs
    raw = adc.read(MCP3201::Channel::SINGLE_0);

    // update the spectrum
    spectrum[raw] ++;

    // reset the Sample & Hld at the end of ISR
    resetSampleHold();

    // increase total amount of events
    events ++;
}

void setup(void)
{ 
    // set pin modes and states
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    pinMode(RST_PIN, OUTPUT);
    digitalWrite(RST_PIN, LOW);

    pinMode(INT_PIN, INPUT);

    pinMode(VSPI_CS_PIN, OUTPUT);
    digitalWrite(VSPI_CS_PIN, HIGH);

    // initialize UART
    Serial.begin(115200);

    // initialize SPI interface for MCP3201
    SPISettings settings(ADC_CLK, MSBFIRST, SPI_MODE0);
    SPI.begin();
    SPI.beginTransaction(settings);

    // ISR initialization
    resetSampleHold();
    attachInterrupt(digitalPinToInterrupt(INT_PIN), handleInterrupt, RISING);

    // Wifi initialization
    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);
    WiFi.setAutoReconnect(true);
    WiFi.onEvent(WiFiEvent);

    //wm.resetSettings();

    wifiManager.setConfigPortalBlocking(false);
    wifiManager.setConfigPortalTimeout(AP_TIMEOUT);

    if(!wifiManager.autoConnect(AP_NAME))
    {
        Serial.println("Configportal running");
    }
    else
    {
        // access the webserver with URL "gamma.local"
        if (!MDNS.begin("gamma"))
        {
            Serial.println("Error setting up MDNS responder!");
            while(1)
            {
                delay(1000);
            }
        }

        // initialize webserver URLs
        server.on("/clear", HTTP_GET, [](AsyncWebServerRequest *request) {
            AsyncResponseStream *response = request->beginResponseStream("text/html");

            for (int i = 0; i < ADC_CHANNELS; i ++)
            {
                spectrum[i] = 0u;
            }
            last_timestamp = millis();
            events = 0ul;

            response->println("<html>");
            response->println("  <head>"); 
            response->println("  </head>"); 
            response->println("  <body>");
            response->println("    <p>Current measurement data has been cleared!</p>");
            response->println("  </body>");
            response->println("</html>");
            request->send(response);
        });

        server.on("/json", HTTP_GET, [](AsyncWebServerRequest *request) {
            AsyncResponseStream *response = request->beginResponseStream("application/json");
            DynamicJsonDocument json(70000);

            timeSinceReset(timebuf);
            minutes = minutesSinceReset();

            json["time"] = timebuf;
            json["minutes"] = minutes;
            json["events"] = events;
            json["avr_cpm"] = events / minutes;
            for (int i = 0; i < ADC_CHANNELS; i ++)
            { 
                json["data"][i] = spectrum[i];
            }

            serializeJson(json, *response);
            request->send(response);
        });

        server.on("/spectrum", HTTP_GET, [](AsyncWebServerRequest *request) {
            AsyncResponseStream *response = request->beginResponseStream("text/html");

            timeSinceReset(timebuf);

            response->println("<html>");
            response->println("  <head>");
            response->println("    <script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>");
            response->println("    <script type=\"text/javascript\">");

            response->println("      google.charts.load('current', {'packages':['corechart']});");
            response->println("      google.charts.setOnLoadCallback(drawChart);");

            response->println("      function lowPassZeroPhase(input, output, smoothing) {");
            response->println("        var temp = new Array(input.length);");
            response->println("        var value;");
            response->println("        var in_len = input.length;");
            response->println("        value = input[0];");
            response->println("        for (var i = 1; i < in_len; i++) {");
            response->println("          var currentValue = input[i];");
            response->println("          value += (currentValue - value) / smoothing;");
            response->println("          temp[i] = value;");
            response->println("        }");
            response->println("        value = input[in_len - 1];");
            response->println("        for (var i = 1; i < in_len; i++) {");
            response->println("          var currentValue = input[in_len - 1 - i];");
            response->println("          value += (currentValue - value) / smoothing;");
            response->println("          output[in_len - 1 - i] = (temp[in_len - 1 - i] + value) / 2.0;");
            response->println("        }");
            response->println("      }");

            response->println("      function drawChart() {");
            response->print  ("        var count_raw = [");

            minutes = minutesSinceReset();
            for (int i = 0; i < ADC_CHANNELS; i ++)
            {
                response->printf("%d, ", spectrum[i]);
            }

            response->println("          ];");
            response->println("        var cpm_raw = new Array(count_raw.length);");
            response->println("        var cpm_filt = new Array(count_raw.length);");

            response->printf ("        for(i = 0; i < %d; i++) {\n", ADC_CHANNELS);
            response->printf ("          cpm_raw[i] = count_raw[i] / %.2f;\n", minutes);
            response->println("        }");

            response->println("        lowPassZeroPhase(cpm_raw, cpm_filt, 10);");

            response->println("        var data = new google.visualization.DataTable();");
            response->println("        data.addColumn('number', 'channel');");
            response->println("        data.addColumn('number', 'cpm raw');");
            response->println("        data.addColumn('number', 'cpm filtered');");

            response->printf ("        for(i = 0; i < %d; i++) {\n", ADC_CHANNELS);
            response->println("          data.addRow([i, cpm_raw[i], cpm_filt[i]]);");
            response->println("        }");

            response->println("        var options = {");
            response->printf ("          title: 'Gamma Spectrum  -  time elapsed: %s  -  total events: %d  -  average cpm: %.1f',\n", timebuf, events, events / minutes);
            response->println("          curveType: 'none',");
            response->println("          width: 2000,");
            response->println("          height: 1000,");
            response->println("          vAxis: { scaleType: 'log', viewWindow: { min: 0.0001, max: 1}},");
            response->println("          legend: { position: 'bottom' }");
            response->println("        };");

            response->println("        var chart = new google.visualization.LineChart(document.getElementById('gamma_spectrum'));");
            response->println("        chart.draw(data, options);");
            response->println("      }");

            response->println("    </script>");
            response->println("  </head>"); 
            response->println("  <body>");
            response->println("    <div id=\"gamma_spectrum\" style=\"width: 2000px; height: 1000px\"></div>");
            response->println("    <a href=\"/clear\"\"><button>Clear Measurement</button></a>");
            response->println("  </body>");
            response->println("</html>");
            request->send(response);
            yield();
        });

        // start the webserver
        server.begin();

        // add service to MDNS-SD
        MDNS.addService("http", "tcp", 80);
    }
}

void loop(void)
{
    static uint32_t last_exec = 0ul;

    // process wifimanager when in non-blocking mode
    wifiManager.process();

    // reset sample & hold and LED handling
    if (micros() - last_exec >= 500ul)
    {
        // reset Sample & Hold every 500 µs
        resetSampleHold();

        // switch off LED after 100 ms
        if (led_time > 0u)
        {
          led_time --;
        }
        if (led_time == 0u)
        {
          digitalWrite(LED_PIN, LOW);
        }

        last_exec = micros();
    }

    yield();
}
