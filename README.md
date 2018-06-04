# vscode_stm32f1
这是一个基于GCC编译器的VisualStudioCode stm32f103 项目

添加类 led，serial 文件
添加了对 printf float 的支持


用STM32CubeMX选择makefile创建项目
然后把ins和src文件夹下的文件拷贝到本项目同名目录下
拷贝 startup_stm32fxxx.s 和 STM32Fxxxxx_FLASH.ld 到Drivers
根据makefile文件更改 c_cpp-properties.json 和 launch.json 文件中的一些选项即可
