// The 3pi include file must be at the beginning of any program that
// uses the Pololu AVR library and 3pi.
#include <pololu/3pi.h>

// This include file allows data to be stored in program space.  The
// ATmega168 has 16k of program space compared to 1k of RAM, so large
// pieces of static data should be stored in program space.
#include <avr/pgmspace.h>

#include <stdlib.h>
#include "weights.h"
#include "logic.h"

// Introductory messages.  The "PROGMEM" identifier causes the data to
// go into program space.
const char welcome_line1[] PROGMEM = " Pololu";
const char welcome_line2[] PROGMEM = "3\xf7 Robot";
const char demo_name_line1[] PROGMEM = "Maze";
const char demo_name_line2[] PROGMEM = "solver";

// A couple of simple tunes, stored in program space.
const char welcome[] PROGMEM = ">g32>>c32";
const char go[] PROGMEM = "L16 cdegreg4";

// Data for generating the characters used in load_custom_characters
// and display_readings.  By reading levels[] starting at various
// offsets, we can generate all of the 7 extra characters needed for a
// bargraph.  This is also stored in program space.
const char levels[] PROGMEM = {
	0b00000,
	0b00000,
	0b00000,
	0b00000,
	0b00000,
	0b00000,
	0b00000,
	0b11111,
	0b11111,
	0b11111,
	0b11111,
	0b11111,
	0b11111,
	0b11111
};

// This function loads custom characters into the LCD.  Up to 8
// characters can be loaded; we use them for 7 levels of a bar graph.
void load_custom_characters()
{
	lcd_load_custom_character(levels+0,0); // no offset, e.g. one bar
	lcd_load_custom_character(levels+1,1); // two bars
	lcd_load_custom_character(levels+2,2); // etc...
	lcd_load_custom_character(levels+3,3);
	lcd_load_custom_character(levels+4,4);
	lcd_load_custom_character(levels+5,5);
	lcd_load_custom_character(levels+6,6);
	clear(); // the LCD must be cleared for the characters to take effect
}

// This function displays the sensor readings using a bar graph.
void display_readings(const unsigned int *calibrated_values)
{
	unsigned char i;

	for(i=0;i<5;i++) {
		// Initialize the array of characters that we will use for the
		// graph.  Using the space, an extra copy of the one-bar
		// character, and character 255 (a full black box), we get 10
		// characters in the array.
		const char display_characters[10] = {' ',0,0,1,2,3,4,5,6,255};

		// The variable c will have values from 0 to 9, since
		// calibrated values are in the range of 0 to 1000, and
		// 1000/101 is 9 with integer math.
		char c = display_characters[calibrated_values[i]/101];

		// Display the bar graph character.
		print_character(c);
	}
}

// Initializes the 3pi, displays a welcome message, calibrates, and
// plays the initial music.
void initialize()
{
	unsigned int counter; // used as a simple timer
	unsigned int sensors[5]; // an array to hold sensor values

	// This must be called at the beginning of 3pi code, to set up the
	// sensors.  We use a value of 2000 for the timeout, which
	// corresponds to 2000*0.4 us = 0.8 ms on our 20 MHz processor.
	pololu_3pi_init(2000);
	load_custom_characters(); // load the custom characters
	
	// Play welcome music and display a message
	print_from_program_space(welcome_line1);
	lcd_goto_xy(0,1);
	print_from_program_space(welcome_line2);
	play_from_program_space(welcome);
	delay_ms(1000);

	clear();
	print_from_program_space(demo_name_line1);
	lcd_goto_xy(0,1);
	print_from_program_space(demo_name_line2);
	delay_ms(1000);

	// Display battery voltage and wait for button press
	while(!button_is_pressed(BUTTON_B))
	{
		int bat = read_battery_millivolts();

		clear();
		print_long(bat);
		print("mV");
		lcd_goto_xy(0,1);
		print("Press B");

		delay_ms(100);
	}
	
	//new code for better start
	clear();
	print("Init");
	
	// Always wait for the button to be released so that 3pi doesn't
	// start moving until your hand is away from it.
	wait_for_button_release(BUTTON_B);
	delay_ms(1000);

	// Auto-calibration: turn right and left while calibrating the
	// sensors.
	for(counter=0;counter<80;counter++)
	{
		if(counter < 20 || counter >= 60)
			set_motors(40,-40);
		else
			set_motors(-40,40);

		// This function records a set of sensor readings and keeps
		// track of the minimum and maximum values encountered.  The
		// IR_EMITTERS_ON argument means that the IR LEDs will be
		// turned on during the reading, which is usually what you
		// want.
		calibrate_line_sensors(IR_EMITTERS_ON);

		// Since our counter runs to 80, the total delay will be
		// 80*20 = 1600 ms.
		delay_ms(20);
	}
	set_motors(0,0);		

	// Play music and wait for it to finish before we start driving.
	play_from_program_space(go);
	while(is_playing());
}

long long int* calculate_wheelvalues(unsigned int sensors[5], const int weights[5][2])
{
	long long int* values = malloc(2*sizeof(long long int));
	values[0] = 0;
	values[1] = 0;
	for(int i = 0; i < 5; i++){
		values[0] += sensors[i] * weights[i][0];
		values[1] += sensors[i] * weights[i][1];
	}
	values[0] = (long long int)(values[0]/1000);
	values[1] = (long long int)(values[1]/1000);
	
	return values;
}

int sensor_values_all_low(unsigned int sensor[5])
{
	int all_low = 1;
	for(int i = 0; i < 5; i++){
		if(sensor[i] > 50){
			all_low = 0;
		}
	}
	
	return all_low;
}

// This is the main function, where the code starts.  All C programs
// must have a main() function defined somewhere.
int main()
{
	unsigned int sensors[5]; // an array to hold sensor values
	unsigned int counter = 0;
	unsigned int max_speed = 30;
	
	set_motors(0,0);

	// set up the 3pi
	initialize();
	
	long long int* wheel_values = malloc(2*sizeof(long long int));

	// This is the "main loop" - it will run forever.
	while(1)
	{
		free(wheel_values);
		wheel_values = NULL;
		read_line(sensors,IR_EMITTERS_ON);
		if (sensor_values_all_low(sensors)){
			clear();
			print("Not on");
			lcd_goto_xy(0,1);
			print("Line!");
			set_motors(0,0);
			break;
		}
		wheel_values = calculate_wheelvalues(sensors, weights);
		if(wheel_values[0] > max_speed){
			wheel_values[0] = max_speed;
		}
		else if(wheel_values[0] < 10 && wheel_values[0] > 0){
			wheel_values[0] = 0;
		}
		if(wheel_values[1] > max_speed){
			wheel_values[1] = max_speed;
		}
		else if(wheel_values[1] < 10 && wheel_values[1] > 0){
			wheel_values[1] = 0;
		}
		counter++;
		if(counter > 50){
			clear();
			print("Sensors:");
			lcd_goto_xy(0,1);
			display_readings(sensors);
			counter = 0;
		}
		set_motors(wheel_values[0], wheel_values[1]);
		
		handle_stop_condition(wheel_values, sensors);
	}
}

// Local Variables: **
// mode: C **
// c-basic-offset: 4 **
// tab-width: 4 **
// indent-tabs-mode: t **
// end: **
