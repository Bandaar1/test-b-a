import pandas as pd
import chardet

# دالة لاكتشاف الترميز باستخدام chardet
def detect_encoding(filepath):
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# دالة لتحليل الملف
def analyze_file(filepath):
    try:
        # أولاً، محاولة استخدام الترميز الذي تم اكتشافه بواسطة chardet
        encoding = detect_encoding(filepath)
        print(f"تم اكتشاف الترميز: {encoding}")

        # قراءة الملف باستخدام الترميز المكتشف
        df = pd.read_csv(filepath, encoding=encoding, sep=',', on_bad_lines='skip', errors='replace')
        return df

    except FileNotFoundError:
        print(f"الملف غير موجود: {filepath}")
        return None
    except UnicodeDecodeError as e:
        # في حالة حدوث خطأ في فك الترميز، استخدام ترميز بديل مثل windows-1252
        print(f"حدث خطأ في فك الترميز: {e}")
        print("جاري المحاولة باستخدام ترميز windows-1252...")
        
        # محاولة قراءة الملف باستخدام ترميز windows-1252
        try:
            df = pd.read_csv(filepath, encoding='windows-1252', sep=',', on_bad_lines='skip', errors='replace')
            return df
        except Exception as ex:
            print(f"فشل في قراءة الملف باستخدام الترميز البديل: {ex}")
            return None
    except Exception as ex:
        print(f"حدث خطأ غير متوقع: {ex}")
        return None

# مثال لاستخدام الدالة:
filepath = 'path_to_your_file.csv'
result = analyze_file(filepath)

if result is not None:
    print(result)
