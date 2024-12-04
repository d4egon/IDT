from nine_lang_interpreter_core import NineLangInterpreter

interpreter = NineLangInterpreter()

# Test Python
python_code = "print('Hello from Python!')"
print(interpreter.execute("$run_python", python_code))

# Test Java
java_code = '''
public class TempProgram {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
    }
}
'''
print(interpreter.execute("$run_java", java_code))

# Test C
c_code = '''
#include <stdio.h>
int main() {
    printf("Hello from C!\\n");
    return 0;
}
'''
print(interpreter.execute("$run_c", c_code))