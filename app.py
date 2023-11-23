from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


app = Flask(__name__)

@app.route('/')
def index():
    # COMPAS 데이터셋 불러오기
    file_path = 'cox-violent-parsed_filt_usable.csv'  # 실제 파일 경로로 수정해주세요
    df = pd.read_csv(file_path)

    # 성별과 재범 발생 여부 컬럼 선택
    gender_recid = df[['sex', 'is_recid']]

    # 성별과 재범 발생 여부에 대한 교차표 생성
    cross_table_gender = pd.crosstab(gender_recid['sex'], gender_recid['is_recid'])

    # 교차표 시각화 - 성별 vs 재범 발생 여부
    plt.figure(figsize=(8, 6))
    sns.heatmap(cross_table_gender, annot=True, cmap='coolwarm', fmt='d')
    plt.title('Gender vs Recidivism')
    plt.xlabel('Recidivism')
    plt.ylabel('Gender')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    gender_plot_url = base64.b64encode(img.getvalue()).decode()

    # 나이와 재범 발생 여부 컬럼 선택
    age_recid = df[['age', 'is_recid']]

    # 나이와 재범 발생 여부에 대한 교차표 생성
    cross_table_age = pd.crosstab(age_recid['age'], age_recid['is_recid'])

    # 교차표 시각화 - 나이 vs 재범 발생 여부
    plt.figure(figsize=(12, 6))
    sns.heatmap(cross_table_age, cmap='coolwarm', annot=True, fmt='d')
    plt.title('Age vs Recidivism')
    plt.xlabel('Recidivism')
    plt.ylabel('Age')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    age_plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', gender_plot_url=gender_plot_url, age_plot_url=age_plot_url)

if __name__ == '__main__':
    app.run(debug=True)
