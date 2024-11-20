import pandas as pd
import os

# بيانات نموذجية
data = {
    'TransactionID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'AccountID': [12345, 12345, 12346, 12347, 12348, 12349, 12350, 12351, 12352, 12353],
    'Amount': [10000, 20000, 50000, 1000, 100000, 5000, 200000, 30000, 15000, 250000],
    'TransactionType': ['Deposit', 'Withdraw', 'Deposit', 'Withdraw', 'Withdraw', 'Deposit', 'Withdraw', 'Deposit', 'Withdraw', 'Withdraw'],
    'Timestamp': ['2024-11-20 10:00:00', '2024-11-20 11:30:00', '2024-11-20 12:00:00', 
                  '2024-11-20 13:30:00', '2024-11-20 14:00:00', '2024-11-20 15:00:00', 
                  '2024-11-20 16:00:00', '2024-11-20 17:00:00', '2024-11-20 18:30:00', 
                  '2024-11-20 19:00:00'],
    'Location': ['New York', 'New York', 'Los Angeles', 'Boston', 'Chicago', 'San Francisco', 
                 'Miami', 'Chicago', 'New York', 'San Francisco'],
    'Category': ['Transfer', 'ATM', 'Transfer', 'ATM', 'Wire Transfer', 'Transfer', 
                 'Wire Transfer', 'ATM', 'Transfer', 'Wire Transfer']
}

# إنشاء DataFrame
df = pd.DataFrame(data)

# دالة للحصول على نطاق المبالغ المشبوهة من العميل
def get_suspicious_range():
    while True:
        try:
            lower_bound = float(input("أدخل الحد الأدنى للمبلغ المشبوه: "))
            upper_bound = float(input("أدخل الحد الأعلى للمبلغ المشبوه: "))
            if lower_bound > upper_bound:
                print("الحد الأدنى يجب أن يكون أقل من الحد الأعلى. حاول مرة أخرى.")
            else:
                return lower_bound, upper_bound
        except ValueError:
            print("الرجاء إدخال أرقام صحيحة.")

# الحصول على نطاق المبالغ المشبوهة من العميل
lower_bound, upper_bound = get_suspicious_range()

# تعريف شرط العمليات المشبوهة بناءً على النطاق المدخل
def is_suspicious(row):
    if lower_bound <= row['Amount'] <= upper_bound:  # المعاملات بين النطاق المدخل
        return True
    if row['TransactionType'] == 'Wire Transfer':  # المعاملات من نوع Wire Transfer
        return True
    if row['TransactionType'] == 'Transfer' and row['Amount'] > 20000:  # معاملات التحويل بأكثر من 20,000
        return True
    return False

# تصنيف العمليات المشبوهة
suspicious_transactions = df[df.apply(is_suspicious, axis=1)]

# تحديد اسم الملف المشبوه
suspicious_file = 'suspicious_transactions.xlsx'

# حفظ العمليات المشبوهة في ملف Excel
suspicious_transactions.to_excel(suspicious_file, index=False, engine='openpyxl')

# التحقق من وجود الملف بعد حفظه
if os.path.exists(suspicious_file):
    print(f"تم إنشاء ملف العمليات المشبوهة بنجاح: {suspicious_file}")
else:
    print("فشل في إنشاء الملف.")

