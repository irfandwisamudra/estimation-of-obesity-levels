from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('random_forest.sav', 'rb'))

def validasi_inputan(form_data):
    errors = {}

    for field in ["Gender", "Age", "Height", "Weight", "family_history", "FAVC", "FCVC", 
                  "NCP", "CAEC", "SMOKE", "CH20", "SCC", "FAF", "TUE", "CALC", "CAEC", "MTRANS"]:
        if not form_data.get(field):
            errors[field] = f"{field} tidak boleh kosong."
    return errors

def validate_data(record):
    errors = {}
    if record["Gender"] < 0 or record["Gender"] > 1:
        errors["Gender"] = "Jenis kelamin harus sesuai pilihan"
    if record["Age"] < 10 or record["Age"] > 70:
        errors["Age"] = "Umur harus diantara 10 dan 70 tahun"
    if record["Height"] < 1 or record["Height"] > 2.5:
        errors["Height"] = "Tinggi harus diantara 1 dan 2.5 meter"
    if record["Weight"] < 30 or record["Weight"] > 200:
        errors["Weight"] = "Berat harus diantara 30 dan 200 kg"
    if record["family_history"] < 0 or record["family_history"] > 1:
        errors["family_history"] = "Riwayat keluarga harus sesuai pilihan"
    if record["FAVC"] < 0 or record["FAVC"] > 1:
        errors["FAVC"] = "Konsumsi sayur harus sesuai pilihan"
    if record["NCP"] < 1 or record["NCP"] > 3:
        errors["NCP"] = "Konsumsi makanan harus sesuai pilihan"
    if record["FCVC"] < 1 or record["FCVC"] > 3:
        errors["FCVC"] = "Konsumsi buah harus sesuai pilihan"
    if record["CH20"] < 1 or record["CH20"] > 4:
        errors["CH20"] = "Jumlah air minum harus sesuai pilihan"
    if record["TUE"] < 0 or record["TUE"] > 2:
        errors["TUE"] = "Penggunaan perangkat teknologi harus sesuai pilihan"
    if record["CALC"] < 0 or record["CALC"] > 3:
        errors["CALC"] = "Tingkat menghindari makanan berkalori tinggi harus sesuai pilihan"
    if record["CAEC"] < 0 or record["CAEC"] > 3:
        errors["CAEC"] = "Konsumsi alkohol harus sesuai pilihan"
    if record["MTRANS"] < 0 or record["MTRANS"] > 4:
        errors["MTRANS"] = "Metode transportasi harus sesuai pilihan"
    return errors

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = {}
    risk = None
    if request.method == 'POST':
        form_data = request.form

        # Validasi inputan
        errors = validasi_inputan(form_data)
        
        if errors:
            return render_template('index.html', errors=errors)
        
        # Buat record untuk validasi data
        record = {
            "Gender": int(form_data['Gender']),
            "Age": int(form_data['Age']),
            "Height": float(form_data['Height']),
            "Weight": float(form_data['Weight']),
            "family_history": int(form_data['family_history']),
            "FAVC": int(form_data['FAVC']),
            "FCVC": int(form_data['FCVC']),
            "NCP": int(form_data['NCP']),
            "CAEC": int(form_data['CAEC']),
            "SMOKE": int(form_data['SMOKE']),
            "CH20": int(form_data['CH20']),
            "SCC": int(form_data['SCC']),
            "FAF": int(form_data['FAF']),
            "TUE": int(form_data['TUE']),
            "CALC": int(form_data['CALC']),
            "MTRANS": int(form_data['MTRANS'])
        }
        
        # Validasi data
        data_errors = validate_data(record)
        if data_errors:
            return render_template('index.html', errors=data_errors)
        
        # Prediksi menggunakan model
        input_data = [[record["Gender"], record["Age"], record["Height"], record["Weight"], record["family_history"], record["FAVC"], record["FCVC"], record["NCP"], record["CAEC"], record["SMOKE"], record["CH20"], record["SCC"], record["FAF"], record["TUE"], record["CALC"], record["MTRANS"]]]
        
        try:
            prediction = model.predict(input_data)
            risk_levels = {
                1: 'Insufficient Weight (Kurus)',
                2: 'Normal Weight (Normal)',
                3: 'Overweight Level I (Kelebihan Berat Badan Tingkat I)',
                4: 'Overweight Level II (Kelebihan Berat Badan Tingkat II)',
                5: 'Obesity Type I (Obesitas Tipe I)',
                6: 'Obesity Type II (Obesitas Tipe II)',
                7: 'Obesity Type III (Obesitas Tipe III)'
            }
            risk = risk_levels[prediction[0]]
        except Exception as e:
            errors['prediction'] = 'Terjadi kesalahan saat memproses data. Silakan coba lagi.'
            return render_template('index.html', errors=errors)
        
    return render_template('index.html', errors=errors, risk=risk)

if __name__ == '__main__':
    app.run(debug=True)
