import signal, time
import sys


# https://blog.csdn.net/z5z5z5z56/article/details/107586391
# SIGABORT 进程停止运行
# SIGALRM 警告钟
# SIGFPE 浮点运算例外
# SIGHUP 系统挂断
# SIGILL 非法指令
# SIGINT 终端中断
# SIGKILL 停止进程(此信号不能被忽略或捕获)
# SIGPIPE 向没有读者的管道
# SIGSEGV 无效内存段访问
# 信号名称 描述
# SIGQUIT 终端退出ctrl+
# SIGTERM 正常终止
# SIGUSR1 用户定义信号1
# SIGUSR2 用户定义信号2
# SIGCHLD 子进程已经停止或退出
# SIGCONT 如果被停止则继续执行
# SIGSTOP 停止执行
# SIGTSTP 终端停止信号
# SIGTOUT 后台进程请求进行写操作
# SIGTTIN 后台进程请求进行读操作
# 进程可以通过三种方式来响应一个信号：
# （1）忽略信号，即对信号不做任何处理，其中，有两个信号不能忽略：SIGKILL及SIGSTOP；
# （2）捕捉信号。定义信号处理函数，当信号发生时，执行相应的处理函数；
# （3）执行缺省操作，Linux对每种信号都规定了默认操作。注意，进程对实时信号的缺省反应是进程终止。

def term_sig_handler(signum, frame):
    print("中断发生。")
    # 需要最后做的事情
    print(signum)
    print("执行最后的清理工作。")
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, term_sig_handler)  # ctrl + c
    signal.signal(signal.SIGTERM, term_sig_handler)  # kill + pid
    signal.signal(signal.SIGHUP, term_sig_handler)  #
    # signal.signal(signal.SIGKILL) can't catch
    while True:
        print("RUNNING")
        time.sleep(3)
