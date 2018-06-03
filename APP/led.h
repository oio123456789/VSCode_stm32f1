

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef _LED_H
#define _LED_H

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

#define LED_GPIO   				GPIOB
#define LED_PIN     			GPIO_PIN_9
#define LED_GPIO_CLK_ENABLE     __HAL_RCC_GPIOB_CLK_ENABLE()

class Led_Class
{
		
	GPIO_TypeDef * 	GPIOx;
	uint16_t 				PIN_x;
	GPIO_PinState 	state;	
	public:
		Led_Class(GPIO_TypeDef* GPIOx = LED_GPIO,uint16_t PIN_x = LED_PIN)
		{			
			Init(GPIOx,PIN_x);
		}
		void Init(GPIO_TypeDef* GPIOx,uint16_t PIN_x){
		
			GPIO_InitTypeDef GPIO_InitStruct;

			this->GPIOx = GPIOx;
			this->PIN_x = PIN_x;
			/* GPIO Ports Clock Enable */
			//__HAL_RCC_GPIOC_CLK_ENABLE();  
			LED_GPIO_CLK_ENABLE;
			/*Configure GPIO pin Output Level */
			HAL_GPIO_WritePin(GPIOx, PIN_x, GPIO_PIN_RESET);

			/*Configure GPIO pin : PC2 */
			GPIO_InitStruct.Pin = PIN_x;
			GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
			GPIO_InitStruct.Pull = GPIO_PULLDOWN;
			GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
			HAL_GPIO_Init(GPIOx, &GPIO_InitStruct);	
		};
		void Set(uint8_t pin_state){
			if(pin_state== GPIO_PIN_RESET)	
				state = GPIO_PIN_RESET;	
			else
				state = GPIO_PIN_SET;	
			HAL_GPIO_WritePin(GPIOx,PIN_x,state);		
		};
		void Change(void){			
			if(state == GPIO_PIN_RESET)	
				state = GPIO_PIN_SET;			
			else
				state = GPIO_PIN_RESET;
			HAL_GPIO_WritePin(GPIOx,PIN_x,state);			
		};
};
/* USER CODE END Prototypes */

Led_Class led_class;
#define LED_SET  			led_class.Set
#define LED_CHANGE 		led_class.Change()
#endif
/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
