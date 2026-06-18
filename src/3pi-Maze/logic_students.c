#include <pololu/3pi.h>
#include "logic.h"

// set_motors(x, y);                        Sets the speed and direction of the left and right motors using x and y values (use values between -50 and 50).
// delay_ms(x);                             Waits for x milliseconds before the program continues (the robot keeps moving if it was already moving, and stays still if it was stopped).
// read_line(sensors, IR_EMITTERS_ON);      Reads line sensor values into sensors with IR emitters turned on.
// If-Else-Logic: https://www.programiz.com/c-programming/c-if-else-statement
// While-Loop: https://www.programiz.com/c-programming/c-do-while-loops

void handle_stop_condition(long long int *wheel_values, unsigned int *sensors)
{
    return;
}
