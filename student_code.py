ten,sl,dongia = map(str, input().split())
tongia = int(dongia) * int(sl)
vat = tongia * 0.1
tongcong = tongia + vat
print(f'''
+------------------------------+
|      Siêu thị Bonlao         |
+------------------------------+
| Tên sản phẩm: {ten:<15}|
| Số lượng:     {sl:<15}|
| Đơn giá:      {dongia:<15}|
+------------------------------+
| Tổng tiền:    {tongia:<15}|
| VAT (10%):    {vat:<15.2f}|
+------------------------------+
| Tổng cộng:    {tongcong:<15}|
+------------------------------+
''')