# cau2.py - Giao diện "Quản lý sách thư viện" (tkinter)
import tkinter as tk
from tkinter import ttk, messagebox


# ---------- Các hàm xử lý (tái sử dụng từ Câu 1) ----------
def them_sach(danh_sach, ma, ten, gia, soluong):
    danh_sach.append({"ma": ma, "ten": ten, "gia": gia, "soluong": soluong})


def tim_kiem_theo_ten(danh_sach, tu_khoa):
    tu_khoa = tu_khoa.strip().lower()
    return [s for s in danh_sach if tu_khoa in s["ten"].lower()]


def dinh_dang(s):
    """Định dạng: S001 - Lập trình Python cơ bản - 95000đ - SL: 40"""
    return f"{s['ma']} - {s['ten']} - {s['gia']}đ - SL: {s['soluong']}"


# ---------- Giao diện ----------
class UngDungQuanLySach(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý sách thư viện")
        self.geometry("620x520")
        self.minsize(560, 480)

        self.danh_sach = []
        # Dữ liệu mẫu
        them_sach(self.danh_sach, "S001", "Lập trình Python cơ bản", 95000, 40)
        them_sach(self.danh_sach, "S002", "Cấu trúc dữ liệu và giải thuật", 120000, 6)
        them_sach(self.danh_sach, "S003", "Nhập môn trí tuệ nhân tạo", 150000, 25)

        self.tao_giao_dien()
        self.hien_thi(self.danh_sach)

    def tao_giao_dien(self):
        # --- a) Form nhập liệu ---
        frm_nhap = ttk.LabelFrame(self, text="Thông tin sách", padding=10)
        frm_nhap.pack(fill="x", padx=10, pady=(10, 5))
        frm_nhap.columnconfigure(1, weight=1)

        self.var_ma = tk.StringVar()
        self.var_ten = tk.StringVar()
        self.var_gia = tk.StringVar()
        self.var_sl = tk.StringVar()

        cac_truong = [
            ("Mã sách:", self.var_ma),
            ("Tên sách:", self.var_ten),
            ("Giá (đ):", self.var_gia),
            ("Số lượng:", self.var_sl),
        ]
        for i, (nhan, var) in enumerate(cac_truong):
            ttk.Label(frm_nhap, text=nhan).grid(
                row=i, column=0, sticky="w", padx=(0, 10), pady=4
            )
            ttk.Entry(frm_nhap, textvariable=var).grid(
                row=i, column=1, sticky="ew", pady=4
            )

        frm_nut = ttk.Frame(frm_nhap)
        frm_nut.grid(
            row=len(cac_truong), column=0, columnspan=2, pady=(8, 0)
        )
        ttk.Button(
            frm_nut, text="Thêm sách", command=self.them_sach_click
        ).pack(side="left", padx=5)
        ttk.Button(
            frm_nut, text="Xóa form", command=self.xoa_form
        ).pack(side="left", padx=5)

        # --- c) Tìm kiếm ---
        frm_tim = ttk.LabelFrame(self, text="Tìm kiếm theo tên", padding=10)
        frm_tim.pack(fill="x", padx=10, pady=5)
        frm_tim.columnconfigure(0, weight=1)

        self.var_tim = tk.StringVar()
        o_tim = ttk.Entry(frm_tim, textvariable=self.var_tim)
        o_tim.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        o_tim.bind("<Return>", lambda e: self.tim_kiem_click())

        ttk.Button(
            frm_tim, text="Tìm kiếm", command=self.tim_kiem_click
        ).grid(row=0, column=1, padx=2)
        ttk.Button(
            frm_tim, text="Hiện tất cả", command=self.hien_tat_ca
        ).grid(row=0, column=2, padx=2)

        # --- Vùng hiển thị danh sách ---
        frm_ds = ttk.LabelFrame(self, text="Danh sách sách", padding=10)
        frm_ds.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        frm_ds.rowconfigure(0, weight=1)
        frm_ds.columnconfigure(0, weight=1)

        self.lst = tk.Listbox(
            frm_ds, font=("Segoe UI", 10), activestyle="none"
        )
        self.lst.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(
            frm_ds, orient="vertical", command=self.lst.yview
        )
        scroll.grid(row=0, column=1, sticky="ns")
        self.lst.config(yscrollcommand=scroll.set)

        self.lbl_trang_thai = ttk.Label(frm_ds, text="")
        self.lbl_trang_thai.grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(6, 0)
        )

    # ---------- Xử lý sự kiện ----------
    def hien_thi(self, ds):
        """Xóa kết quả cũ rồi hiển thị danh sách mới."""
        self.lst.delete(0, tk.END)
        for s in ds:
            self.lst.insert(tk.END, dinh_dang(s))
        self.lbl_trang_thai.config(text=f"Số sách hiển thị: {len(ds)}")

    def xoa_form(self):
        for var in (self.var_ma, self.var_ten, self.var_gia, self.var_sl):
            var.set("")

    # b) + d) Thêm sách có kiểm tra dữ liệu
    def them_sach_click(self):
        ma = self.var_ma.get().strip()
        ten = self.var_ten.get().strip()
        gia_str = self.var_gia.get().strip()
        sl_str = self.var_sl.get().strip()

        if not ma or not ten:
            messagebox.showerror(
                "Lỗi", "Mã sách và Tên sách không được để trống!"
            )
            return

        try:
            gia = int(gia_str)
            if gia < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Lỗi", "Giá phải là số nguyên không âm hợp lệ!"
            )
            return

        try:
            soluong = int(sl_str)
            if soluong < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Lỗi", "Số lượng phải là số nguyên không âm hợp lệ!"
            )
            return

        if any(s["ma"].lower() == ma.lower() for s in self.danh_sach):
            messagebox.showerror("Lỗi", f"Mã sách '{ma}' đã tồn tại!")
            return

        them_sach(self.danh_sach, ma, ten, gia, soluong)

        # Hiển thị lại toàn bộ danh sách và cuộn xuống cuối
        self.var_tim.set("")
        self.hien_thi(self.danh_sach)
        self.lst.see(tk.END)
        self.lst.selection_clear(0, tk.END)
        self.lst.selection_set(tk.END)
        self.xoa_form()

    # c) Tìm kiếm
    def tim_kiem_click(self):
        ket_qua = tim_kiem_theo_ten(self.danh_sach, self.var_tim.get())
        self.hien_thi(ket_qua)

        if not ket_qua:
            self.lbl_trang_thai.config(
                text="Không tìm thấy sách nào phù hợp."
            )

    def hien_tat_ca(self):
        self.var_tim.set("")
        self.hien_thi(self.danh_sach)


if __name__ == "__main__":
    UngDungQuanLySach().mainloop()