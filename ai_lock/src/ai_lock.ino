#include "nn.h"

// Inspired from https://bitbucket.org/dimtass/machine-learning-for-embedded/src/master/code-arduino/


const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
char messageFromPC[numChars] = {0};

float weight_1 = 0.0;
float weight_2 = 0.0;
float weight_3 = 0.0;
int pin = 0;
int key[8] = {0,0,0,0,0,0,0,0};
#define FLAG_LEN 32
// int flag[FLAG_LEN] = {0x66,0x6c,0x7b,0x69,0x74,0x6b,0x6a,0x72};
int flag[FLAG_LEN] = {0x25,0x2f,0x38,0x2a,0x37,0x18,
0x25,0x22,0x35,0x1,0x0,0x13,0x25,
0x3f,0x13,0x2f,0x7c,0x7c,0x20,
0x13,0x2e,0x39,0x38,0x13,0xd,0x1a,
0x1e,0x13,0x24,0x21,0x21,0x31};


boolean newData = false;

double weight_digit_1[3] = {
  9.67299303,
  -0.2078435,
  -4.62963669};
  
double weight_digit_2[3] = {
  9.67299303,
  -0.2078435,
  -4.62963669};
  
double weight_digit_3[3] = {
  9.67299303,
  -0.2078435,
  -4.62963669};
  
double weight_digit_4[3] = {
  9.67299303,
  -0.2078435,
  -4.62963669};

double inputs[8][3] = {
    {0, 0, 0},
    {0, 0, 1},
    {0, 1, 0},
    {0, 1, 1},
    {1, 0, 0},
    {1, 0, 1},
    {1, 1, 0},
    {1, 1, 1},
};


void(* resetFunc) (void) = 0;

void avail_commands()
{
  Serial.println("Available commands.....");
  Serial.println(">LOGIN <PIN>");
  Serial.println(">RESET");
  Serial.println(">HELP");
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);
  
  Serial.println("Booting lock firmware.......");
  avail_commands();
}


void test_neural_network(void)
{
  for (int i=0; i<8; i++) {
    double result = sigmoid(dot(inputs[i], weight_digit_4, 3));
    Serial.print("3 Inputs: ");
    Serial.print(inputs[i][0]);
    Serial.print(' ');
    Serial.print(inputs[i][1]);
    Serial.print(' ');
    Serial.print(inputs[i][2]);
    Serial.print(' ');
    Serial.print("\tFinal Result: ");
    Serial.println(result);
  }
  Serial.println();
}


void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '>';
    char endMarker = '\n';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseSetData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars," ");      // get the first part - the string
    strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
 
    strtokIndx = strtok(NULL, " "); // this continues where the previous call left off
    weight_1 = atof(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, " ");
    weight_2 = atof(strtokIndx);     // convert this part to a float

    strtokIndx = strtok(NULL, " ");
    weight_3 = atof(strtokIndx);     // convert this part to a float
}

//============

void showParsedData() {
    Serial.print("Command ");
    Serial.println(messageFromPC);
    Serial.print("Weight 1\t");
    Serial.println(weight_1);
    Serial.print("Weight 2\t");
    Serial.println(weight_2);
    Serial.print("Weight 3\t");
    Serial.println(weight_3);
}

void setData() {
  Serial.println("Recalibrating weights......");
  weight_digit_4[0] = weight_1;
  weight_digit_4[1] = weight_2;
  weight_digit_4[2] = weight_3;
  Serial.println("Done......");
}


void parseLoginData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars," ");      // get the first part - the string
    strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
 
    strtokIndx = strtok(NULL, " "); // this continues where the previous call left off
    pin = atoi(strtokIndx);     // convert this part to an integer
}

void showLoginData() {
    Serial.print("Command ");
    Serial.println(messageFromPC);
    Serial.print("PIN\t");
    Serial.println(pin);
}

int loginFunc() {
   if (pin == 1009){
   // Serial.print("Key:\t");
   Serial.println("Employee PIN check passed... (ಠ‿ಠ)");
   int key_val = 0;
   for (int i=0; i<8; i++) {
    double result = sigmoid(dot(inputs[i], weight_digit_4, 3));
    if (result > 0.65) {
      key[i] = 1;
    }
    else {
      key[i] = 0;
    }
    key_val = (key_val << 1) | key[i]; 
    // Serial.print(key[i]);
  }
  Serial.println();
  // Try to decode the encrypted string 
  // If contains ictf{ flag print it out 
  //Serial.println(key_val);
  //Serial.println((flag[0] ^ key_val) == 105);
  if (((flag[0] ^ key_val) == 105) && ((flag[1] ^ key_val) == 99) && ((flag[2] ^ key_val) == 116) && ((flag[3] ^ key_val) == 102)) { 
      Serial.print("Congrats: \t");
       for(int i=0;i<FLAG_LEN;i++){
        Serial.print((char) (flag[i] ^ key_val));
       }
        Serial.println();
      }
    else {
      Serial.println("Are you an employee? AI signature doesn't match (ಠ_ಠ)");
    }
  Serial.println();
  return 0;
  }
  else {
  Serial.println("Failed employee PIN check... (ಠ_ಠ)");
  return -1;  
  }
  
}

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        if (strcmp(receivedChars,"PREDICT") == 0) // HIDDEN
        {
          Serial.println("Prediction command detected, printing debug information....");
          Serial.println();
          test_neural_network();
        } // HIDDEN
        else if (strstr(receivedChars,"PARAMSET") != 0) 
        {
          Serial.println("Configuration mode, enter required parameters W1 W2 W3");
          parseSetData();
          showParsedData();
          setData();
        }
        else if (strstr(receivedChars,"LOGIN") != 0){
          parseLoginData();
          //showLoginData();
          loginFunc();
        }
        else if (strcmp(receivedChars,"RESET") == 0){
          resetFunc();
        }
        else if (strcmp(receivedChars,"HELP") == 0){
          avail_commands();
        }
        newData = false;
    }
}
