#include <pololu/3pi.h>
#include "logic.h"

// set_motors(x, y);                        Sets the speed and direction of the left and right motors using x and y values (use values between -50 and 50).
// delay_ms(x);                             Waits for x milliseconds before the program continues (the robot keeps moving if it was already moving, and stays still if it was stopped).
// read_line(sensors, IR_EMITTERS_ON);      Reads line sensor values into sensors with IR emitters turned on.
// If-Else-Logic: https://www.programiz.com/c-programming/c-if-else-statement
// While-Loop: https://www.programiz.com/c-programming/c-do-while-loops

void handle_stop_condition(long long int *wheel_values, unsigned int *sensors)
{
    if(wheel_values[0] == 0 && wheel_values[1] == 0){
        if(sensors[0] > 100 && sensors[4] < 100){
            set_motors(30, 30);
            delay_ms(250);
            set_motors(-30, 30);
            while(1){
                delay_ms(20);
                read_line(sensors, IR_EMITTERS_ON);
                if(sensors[1] > 200 && sensors[2] > 200 && sensors[3] > 200){
                    break;
                }
            }
        }
        else if(sensors[4] > 100 && sensors[0] < 100){
            set_motors(30, 30);
            delay_ms(250);
            set_motors(30, -30);
            while(1){
                delay_ms(20);
                read_line(sensors, IR_EMITTERS_ON);
                if(sensors[1] > 200 && sensors[2] > 200 && sensors[3] > 200){
                    break;
                }
            }
        }
        else{
            set_motors(30, 30);
            delay_ms(250);
            read_line(sensors, IR_EMITTERS_ON);
            if(sensors[0] > 100 && sensors[1] > 0){
                set_motors(-30, 30);
                delay_ms(580);
            }
            else if(sensors[3] > 0 && sensors[4] > 100){
                set_motors(30, -30);
                delay_ms(580);
            }
        }
    }
}