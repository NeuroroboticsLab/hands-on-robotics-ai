DEVICE = atmega328p
MCU = atmega328p
AVRDUDE_DEVICE = m328p
DEVICE ?= atmega168
MCU ?= atmega168
AVRDUDE_DEVICE ?= m168

CFLAGS = -g -Wall -mcall-prologues -mmcu=$(MCU) $(DEVICE_SPECIFIC_CFLAGS) -Os
CFLAGS += -I "../include"
CPP=avr-g++
CC=avr-gcc
OBJ2HEX=avr-objcopy
LDFLAGS=-Wl,-gc-sections -lpololu_$(DEVICE) -Wl,-relax
LDFLAGS += -L../lib

PORT ?= /dev/ttyACM0
AVRDUDE=avrdude
TARGET=line

# --- neu: alle Quellen/Objekte ---
WEIGHTS_FILE = $(if $(SOLUTION),weights.c,weights_students.c)
SRCS = $(TARGET).c $(WEIGHTS_FILE)
OBJS = $(SRCS:.c=.o)

all: $(TARGET).hex

clean:
	rm -f *.o *.hex *.obj

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# --- neu: linke alle Objekte in ein .obj ---
$(TARGET).obj: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(LDFLAGS) -o $@

%.hex: %.obj
	$(OBJ2HEX) -R .eeprom -O ihex $< $@

program: $(TARGET).hex
	$(AVRDUDE) -p $(AVRDUDE_DEVICE) -c avrisp2 -P $(PORT) -U flash:w:$(TARGET).hex
	$(MAKE) clean

