

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef _SERIAL_CCLASS_H
#define _SERIAL_CCLASS_H

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"
#include "usart.h"
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

#define SERIAL_BUFFER_SIZE 256

class Serial_Class
{
  public:
	UART_HandleTypeDef *uart;
	char buffer[SERIAL_BUFFER_SIZE];
	int length;
	int index;

	uint8_t SendData()
	{
		if (length > SERIAL_BUFFER_SIZE)
			length = SERIAL_BUFFER_SIZE;
		return HAL_UART_Transmit(this->uart, (uint8_t *)buffer, length, 0xfff);
	}

  public:
	Serial_Class(UART_HandleTypeDef *uart = &huart1)
	{
		this->uart = uart;
	}
	void Printf(const char *fmt, ...)
	{

		va_list ap;												 //typedef char *va_list; va_list是char型的指针
		va_start(ap, fmt);										 //这个函数的功能是，找到第一个可变形参的地址，并把地址赋给ap
		length = vsnprintf(buffer, SERIAL_BUFFER_SIZE, fmt, ap); //其实这个函数才是核心函数，没研究。。?
		va_end(ap);												 //结束函数
		//-------------------------------------------
		SendData();
	}
	void Println(const char *fmt, ...)
	{

		va_list ap;												 //typedef char *va_list; va_list是char型的指针
		va_start(ap, fmt);										 //这个函数的功能是，找到第一个可变形参的地址，并把地址赋给ap
		length = vsnprintf(buffer, SERIAL_BUFFER_SIZE, fmt, ap); //其实这个函数才是核心函数，没研究。。?
		va_end(ap);												 //结束函数
		//-------------------------------------------
		SendData();
		buffer[0] = '\r';
		buffer[1] = '\n';
		length = 2;
		SendData();
	}

	/*
	Serial_Class &operator<<(const float value)
	{
		//m_value++;	//先增量
		//char *str = __itoa(10,(int16_t)value) ;
		

		return *this; //返回当前对象
	}
	*/

};
/* USER CODE END Prototypes */
///////////////////////////////////////////////////////////////////////////
Serial_Class serial_class;

#define serial serial_class.Printf
///////////////////////////////////////////////////////////////////////////
#endif
/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
