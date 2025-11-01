from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import MutasiBank, MutasiZahir
import pandas as pd
from time import sleep

def home(request):
    bank_count = MutasiBank.objects.count()
    zahir_count = MutasiZahir.objects.count()
    data_ready = bank_count > 0 and zahir_count > 0
    return render(request, 'app/dashboard.html', {'data_ready': data_ready})

def mutasi_bank(request):
    data = MutasiBank.objects.all()
    return render(request, 'app/mutasi_bank.html', {'data': data})

def mutasi_zahir(request):
    data = MutasiZahir.objects.all()
    return render(request, 'app/mutasi_zahir.html', {'data': data})

def laporan(request):
    return render(request, 'app/laporan.html')

def import_data(request):
    # Get file from folder private_file/MUTASI_BANK.xlsx
    file_path = settings.BASE_DIR / 'finance/private_file/MUTASI_BANK.xlsx'
    df = pd.read_excel(file_path)   

    for i, row in df.iterrows():
        #row['Tanggal'] is in 10/21/2025 format 
        #convert to date format yyyy-mm-dd
        row['Tanggal'] = pd.to_datetime(row['Tanggal']).strftime('%Y-%m-%d')

        saldo = 0
        debit = 0
        kredit = 0

        if pd.isna(row['Debet (Uang Keluar)']):
           debit = 0
        else:
           debit = row['Debet (Uang Keluar)']

        if pd.isna(row['Kredit (Uang Masuk)']):
           kredit = 0
        else:
           kredit = row['Kredit (Uang Masuk)']

        if kredit == 0:
            saldo = -debit
        else:
            saldo = kredit

        MutasiBank.objects.create(
            tanggal=row['Tanggal'],
            description=row['Deskripsi'],
            debit=debit,
            kredit=kredit,
            saldo=saldo
        )

    # Get file from folder private_file/ZAHIR.xlsx
    file_path = settings.BASE_DIR / 'finance/private_file/ZAHIR.xlsx'
    df = pd.read_excel(file_path)  

    for i, row in df.iterrows():
        #row['Tanggal'] is in 10/21/2025 format 
        #convert to date format yyyy-mm-dd
        row['Tanggal'] = pd.to_datetime(row['Tanggal']).strftime('%Y-%m-%d')

        saldo = 0
        debit = 0
        kredit = 0

        if pd.isna(row['Debet (Uang Masuk)']):
           debit = 0
        else:
           debit = row['Debet (Uang Masuk)']

        if pd.isna(row['Kredit (Uang Keluar)']):
           kredit = 0
        else:
           kredit = row['Kredit (Uang Keluar)']

        if debit == 0:
            saldo = -kredit
        else:
            saldo = debit

        MutasiZahir.objects.create(
            ref_number=row['Reference Number'],
            ref_code=row['Reference Code'],
            tanggal=row['Tanggal'],
            description=row['Deskripsi'],
            debit=debit,
            kredit=kredit,
            saldo=saldo
        )

    return JsonResponse({'statusCode': 200, 'status': 'ok', 'message': 'Data imported successfully'})

# Create difference report between MutasiBank and MutasiZahir and Response Data as JSON for laporan view
# Filter by date if tanggal is provided in request GET parameter


def generate_report_different(request):
    tanggalFilter = request.GET.get('tanggal', None)

    bank_data = []
    zahir_data = []

    if tanggalFilter:
        # date must be same format as in database yyyy-mm-dd
        try:
            tanggalFilter = pd.to_datetime(tanggalFilter).strftime('%Y-%m-%d')
        except Exception as e:
            return JsonResponse({'statusCode': 400, 'status': 'error', 'message': 'Invalid date format'})

        bank_data = MutasiBank.objects.filter(tanggal__exact=tanggalFilter).values()
        zahir_data = MutasiZahir.objects.filter(tanggal__exact=tanggalFilter).values()
    else:
        # Return error response if no start_date is provided
        return JsonResponse({'statusCode': 400, 'status': 'error', 'message': 'No date provided'})

    bank_df = pd.DataFrame.from_records(bank_data)
    zahir_df = pd.DataFrame.from_records(zahir_data)

    # check if bank_df or zahir_df is empty
    if bank_df.empty or zahir_df.empty:
        return JsonResponse({'statusCode': 404, 'status': 'error', 'message': 'No data found for the selected date'})
    
    # array zahir_df and bank_df must be same, if not same , then array value 0
    if len(bank_df) > len(zahir_df):
        diff = len(bank_df) - len(zahir_df)
        filler = pd.DataFrame([{
            'tanggal': tanggalFilter,
            'description': '-',
            'debit': 0,
            'kredit': 0,
            'saldo': 0
        }] * diff)
        zahir_df = pd.concat([filler,zahir_df], ignore_index=True)
    elif len(zahir_df) > len(bank_df):
        diff = len(zahir_df) - len(bank_df)
        filler = pd.DataFrame([{
            'tanggal': tanggalFilter,
            'description': '-',
            'debit': 0,
            'kredit': 0,
            'saldo': 0
        }] * diff)

        bank_df = pd.concat([filler,bank_df], ignore_index=True)

    # output report data from mutasi bank total and mutasi zahir total
    # Result total between mutasi bank and mutasi zahir is different
    report_data = []

    # create object selisih and detail in report_data
    report_data = {
        'detail': [],
        'selisih': []
    }

    # pastikan kedua dataframe sudah seimbang panjangnya (pakai balance_df sebelumnya)
    for i in range(len(bank_df)):
        bank_row = bank_df.iloc[i]
        zahir_row = zahir_df.iloc[i]

        bank_total = bank_row['saldo']
        zahir_total = zahir_row['saldo']
        difference = "-"

        report_data['detail'].append({
            'tanggal': tanggalFilter,
            'description_bank': bank_row['description'],
            'bank_total': bank_total,
            'description_zahir': zahir_row['description'],
            'zahir_total': zahir_total,
            'difference': difference
        })

    bank_total = bank_df['kredit'].sum() - bank_df['debit'].sum()
    zahir_total = zahir_df['debit'].sum() - zahir_df['kredit'].sum()    

    report_data['selisih'].append({
        'tanggal': tanggalFilter,
        'bank_total': bank_total,
        'zahir_total': zahir_total,
        'difference': bank_total - zahir_total
    })

    print  ("Generated report data:", report_data)

    return JsonResponse({'statusCode': 200, 'status': 'ok', 'data': report_data})
