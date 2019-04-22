import compile_utils
import preprocess
import generate_train

code_path = "data"

if __name__ == "__main__":
    compile_utils.compile(code_path)
    preprocess.process()
    generate_train.process()