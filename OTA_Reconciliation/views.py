from django.shortcuts import render
from django.http import JsonResponse
import os # to veirfy the path of the file
from OTA_Reconciliation.dataClass import UploadFileForm #dataclass to get the filename and verify the file
from datetime import datetime # to generate the files name
from OTA_Reconciliation.murgefiles import booking_mews_merge, expedia_mews_merge, sitminder_mews_merge # merge files

filesname = {
    'booking': '',
    'expedia': '',
    'siteminder': '',
    'mews': ''
}

responseFilesname = {
    'booking': '',
    'expedia': '',
    'siteminder': ''
}

mergingFunctions = {
    'booking': booking_mews_merge,
    'expedia': expedia_mews_merge,
    'siteminder': sitminder_mews_merge
}
#home page
def index(request):
    return render(request, 'home.html')


# handle uploaded file
def handle_uploaded_file(files, ota):
    for index in range(len(files)):
        if not os.path.exists('./files'):
            os.mkdir('./files')
        title = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        if index != 3:
            filename = './files/' + title + '_'+ ota[index] + '.' + files['file' + str(index + 1)].name.split('.')[-1]
        else:
            filename = './files/' + title + '_mews.' + files['file' + str(index + 1)].name.split('.')[-1]
        with open(filename, 'wb+') as destination:
            for chunk in files['file' + str(index + 1)].chunks():
                destination.write(chunk)
        if index != 3:
            filesname[ota[index]] = filename
        else:
            filesname['mews'] = filename


# get the file form the client and send it to handel the file
def uploadfile(request):
    if request.method != 'POST':
        # if the request method is not POST
        return JsonResponse({'success': False, 'message': 'Requested Method is wrong'}, status=400)
    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():  # if the form is not valid
        return JsonResponse({'status': False, 'message': 'Form is not valid'}, status=400)

    # saving the file to the folder
    handle_uploaded_file(request.FILES, [request.POST['ota1'], request.POST['ota2'], request.POST['ota3']])


    if request.POST['ota1'] != '':
        responseFilesname[request.POST['ota1']] = mergingFunctions[request.POST['ota1']](filesname['mews'], filesname[request.POST['ota1']])


    if request.POST['ota2'] != '':
        responseFilesname[request.POST['ota2']] = mergingFunctions[request.POST['ota2']](filesname['mews'], filesname[request.POST['ota2']])


    if request.POST['ota3'] != '':
        responseFilesname[request.POST['ota3']] = mergingFunctions[request.POST['ota3']](filesname['mews'], filesname[request.POST['ota3']])
    
    print(responseFilesname)

    if os.path.exists(f'./static/generatedSheet/{responseFilesname["booking"]}') or os.path.exists(f'./static/generatedSheet/{responseFilesname["expedia"]}') or os.path.exists(f'./static/generatedSheet/{responseFilesname["siteminder"]}'):
        os.remove(filesname["mews"])
        os.remove(filesname["booking"])
        os.remove(filesname["expedia"])
        os.remove(filesname["siteminder"])
        return JsonResponse({'success': True, 'files': responseFilesname}, status=200)


    return JsonResponse({'success': False, 'message': 'Something want wrong!'}, status=400)
    # return JsonResponse({'success': True, 'message': 'File merged successfully', 'file': responseFile}, status=200, safe=False)
