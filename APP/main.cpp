
/* Includes ------------------------------------------------------------------*/

#include "stm32f1xx_hal.h"

#include <main.h>
#include "usart.h"
#include "i2c.h"

#include "led.h"

#include "serial.h"

/* Private variables ---------------------------------------------------------*/

//LED_Class led;

/* Private function prototypes -----------------------------------------------*/

/**
  * @brief  The application entry point.
  *
  * @retval None
  */
int main(void)
{

  /* MCU Configuration----------------------------------------------------------*/
  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();
  /* Configure the system clock */
  SystemClock_Config();
  /* Initialize all configured peripherals */
  MX_USART1_UART_Init(UART_BAUDTATE);
  MX_I2C2_Init();
  /* Initialize all configured peripherals */
  test0();
}

void test0()
{

  float f = 0u;
  uint8_t data[200];
  while (1)
  {
    LED_CHANGE;
    HAL_Delay(100);
    printf("printf int %4d float %4.6f\r\n", (int)f, f);
    serial("serial int %4d float %4.6f\r\n", (int)f, f);
    f += 0.000001;
    if (HAL_UART_Receive_DMA(&huart1, data, 198) == HAL_OK)
    {
      //printf("HAL_UART_Receive_DMA\r\n%s\r\n", data);
      serial("HAL_UART_Receive_DMA\r\n%s\r\n", data);
    }
  }
}

/**
  * @}
  */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
