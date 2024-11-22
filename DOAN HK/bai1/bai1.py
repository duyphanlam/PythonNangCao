import tkinter as tk
from tkinter import messagebox

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Máy Tính Đơn Giản")
        self.geometry("400x700")  # Kích thước cửa sổ
        self.config(bg="#D3E4CD")

        self.result_var = tk.StringVar()
        self.previous_results = []

        # Khu vực hiển thị kết quả hiện tại
        self.display_frame = tk.Frame(self, bg="#E8F6EF")
        self.display_frame.pack(padx=20, pady=20, fill=tk.X)  # Đảm bảo hiển thị đầy đủ

        self.display = tk.Entry(self.display_frame, textvariable=self.result_var, font=("Arial", 24), width=14, borderwidth=2, relief="solid")
        self.display.grid(row=0, column=0, sticky="ew")  # Căn chỉnh để rộng hết chiều ngang

        # Khu vực hiển thị kết quả trước đó
        self.results_label = tk.Label(self.display_frame, text="Kết quả trước đó:", font=("Arial", 14), bg="#E8F6EF", anchor='w')
        self.results_label.grid(row=1, column=0, sticky='w')

        self.previous_results_display = tk.Text(self.display_frame, height=5, width=30, font=("Arial", 12), state='disabled', wrap='word', bg="#F0F0F0")
        self.previous_results_display.grid(row=2, column=0, pady=(5, 0), sticky="nsew")  # Căn chỉnh để rộng hết chiều ngang và chiều dọc

        # Nút xóa kết quả
        self.clear_results_button = tk.Button(self.display_frame, text="Xóa Kết Quả", command=self.clear_previous_results, bg="#FF6B6B", fg="white", font=("Arial", 14))
        self.clear_results_button.grid(row=3, column=0, pady=(10, 0), sticky="ew")  # Đảm bảo nút rộng hết chiều ngang

        # Tạo các nút
        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self, bg="#E8F6EF")
        button_frame.pack()

        # Các nút số và chức năng
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "C", "+",
            "=",
        ]

        # Đặt các nút vào lưới
        row_val = 0
        col_val = 0
        
        for button in buttons:
            cmd = lambda x=button: self.on_button_click(x)  # Gọi hàm cho nút đã nhấn
            button_widget = tk.Button(button_frame, text=button, font=("Arial", 18), width=5, height=2, command=cmd)
            button_widget.grid(row=row_val, column=col_val, padx=5, pady=5)

            col_val += 1
            if col_val > 3:  # Mỗi hàng có 4 nút
                col_val = 0
                row_val += 1

    def on_button_click(self, value):
        # Xóa màn hình
        if value == 'C':
            self.result_var.set("")
        # Tính toán kết quả
        elif value == '=':
            try:
                expression = self.result_var.get()
                # Tính toán biểu thức
                result = eval(expression)
                self.result_var.set(result)
                
                # Lưu kết quả vào danh sách và hiển thị
                self.previous_results.append(f"{expression} = {result}")
                self.display_previous_results()
            except Exception as e:
                messagebox.showerror("Error", "Đã xảy ra lỗi trong tính toán!")
                self.result_var.set("")
        else:
            current_expression = self.result_var.get()
            self.result_var.set(current_expression + value)

    def display_previous_results(self):
        self.previous_results_display.config(state='normal')
        self.previous_results_display.delete(1.0, tk.END)  # Xóa nội dung trước đó
        for result in self.previous_results:
            self.previous_results_display.insert(tk.END, result + "\n")
        self.previous_results_display.config(state='disabled')

    def clear_previous_results(self):
        """Xóa tất cả các kết quả trước đó."""
        self.previous_results = []  # Xóa danh sách kết quả
        self.previous_results_display.config(state='normal')
        self.previous_results_display.delete(1.0, tk.END)  # Xóa văn bản hiện có
        self.previous_results_display.config(state='disabled')

# Khởi chạy ứng dụng
if __name__ == "__main__":
    calculator = Calculator()
    calculator.mainloop()
