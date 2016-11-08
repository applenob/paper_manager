# coding=utf-8
# -----------------colorama模块的一些常量---------------------------
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
# from http://blog.csdn.net/qianghaohao/article/details/52117082
#

from colorama import init, Fore, Back, Style

init(autoreset=True)


class Colored(object):

    def red(self, s):
        #  前景色:红色  背景色:默认
        return Fore.RED + s + Fore.RESET

    def green(self, s):
        #  前景色:绿色  背景色:默认
        return Fore.GREEN + s + Fore.RESET

    def yellow(self, s):
        #  前景色:黄色  背景色:默认
        return Fore.YELLOW + s + Fore.RESET

    def blue(self, s):
        #  前景色:蓝色  背景色:默认
        return Fore.BLUE + s + Fore.RESET

    def magenta(self, s):
        #  前景色:洋红色  背景色:默认
        return Fore.MAGENTA + s + Fore.RESET

    def cyan(self, s):
        #  前景色:青色  背景色:默认
        return Fore.CYAN + s + Fore.RESET

    def white(self, s):
        #  前景色:白色  背景色:默认
        return Fore.WHITE + s + Fore.RESET

    def black(self, s):
        #  前景色:黑色  背景色:默认
        return Fore.BLACK

    def white_green(self, s):
        #  前景色:白色  背景色:绿色
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET

if __name__ == '__main__':
    color = Colored()
    print color.red('I am red!')
    print color.green('I am gree!')
    print color.yellow('I am yellow!')
    print color.blue('I am blue!')
    print color.magenta('I am magenta!')
    print color.cyan('I am cyan!')
    print color.white('I am white!')
    print color.white_green('I am white green!')