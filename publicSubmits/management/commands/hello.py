from django.core.management.base import BaseCommand

class Command(BaseCommand):
    # 帮助文本, 一般备注命令的用途及如何使用。
    help = "Print Hello World!"

    # 核心业务逻辑
    def handle(self, *args, **options):
        self.stdout.write('Hello World!') # **注意**：当你使用管理命令并希望在控制台输出指定信息时，你应该使用`self.stdout`和`self.stderr`方法，而不能直接使用python的`print`方法。另外，你不需要在消息的末尾加上换行符，它将被自动添加。