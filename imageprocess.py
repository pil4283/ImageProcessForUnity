import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import math

# 이미지 크기를 4의 배수로 조정
def adjust_to_multiple_of_four(value):
    remainder = value % 4
    if remainder == 0:
        return value
    elif remainder <= 2:
        return value - remainder  # Round down
    else:
        return value + (4 - remainder)  # Round up

def resize_image_to_multiple_of_four(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        new_width = adjust_to_multiple_of_four(width)
        new_height = adjust_to_multiple_of_four(height)
        resized_img = img.resize((new_width, new_height))
        return resized_img

# 폴더 내 모든 이미지 처리
def process_folder_recursive(folder_path, overwrite):
    for root, _, files in os.walk(folder_path):  # 하위 폴더 포함
        for filename in files:
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp')):
                file_path = os.path.join(root, filename)
                resized_img = resize_image_to_multiple_of_four(file_path)

                if overwrite:
                    resized_img.save(file_path)  # 원본 파일 덮어쓰기
                else:
                    new_file_path = os.path.join(root, f"resized_{filename}")  # 덮어쓰지않으면 파일명앞에 resized_(기본값) 추가
                    resized_img.save(new_file_path)

# 변환시킬 폴더 선택
def select_folder(entry):
    folder_path = filedialog.askdirectory(title="폴더 선택")
    if folder_path:
        entry.delete(0, tk.END)  # 기존 텍스트 덮어쓰기
        entry.insert(0, folder_path) 

# 변환 버튼 클릭
def start_conversion(entry, overwrite_var):
    folder_path = entry.get()  
    overwrite = overwrite_var.get()

    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("오류", "유효한 폴더 경로를 입력하거나 선택하세요.")
        return

    try:
        process_folder_recursive(folder_path, overwrite)
        messagebox.showinfo("완료", "이미지 변환 작업이 완료되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"작업 중 오류가 발생했습니다: {e}")

def create_gui():
    root = tk.Tk()
    root.title("이미지 변환 도구")

    # 폴더 선택 
    folder_label = tk.Label(root, text="폴더 경로:")
    folder_label.grid(row=0, column=0, padx=10, pady=10)

    folder_entry = tk.Entry(root, width=40)
    folder_entry.grid(row=0, column=1, padx=10, pady=10)

    folder_button = tk.Button(root, text="폴더 선택", command=lambda: select_folder(folder_entry))
    folder_button.grid(row=0, column=2, padx=10, pady=10)

    # 덮어쓰기 여부
    overwrite_var = tk.BooleanVar()
    overwrite_var.set(True) 
    overwrite_checkbox = tk.Checkbutton(root, text="이미지 덮어쓰기", variable=overwrite_var)
    overwrite_checkbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # 변환 버튼
    convert_button = tk.Button(root, text="변환 시작", command=lambda: start_conversion(folder_entry, overwrite_var))
    convert_button.grid(row=2, column=0, columnspan=3, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()