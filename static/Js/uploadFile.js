fileCount = 0;
document.getElementById('form').onsubmit = (e) => {
    e.preventDefault();

    // check creating form data
    const formData = new FormData(document.getElementById('form'));
    const xhr = new XMLHttpRequest();
    document.getElementById('loader').classList.add('active');
    xhr.onreadystatechange = () => {

        // check if request is completed
        if (xhr.readyState === 4) {
            const response = JSON.parse(xhr.responseText);
            document.getElementById('loader').classList.remove('active');
            // check if request is successful
            // notifing user about client side error
            if (xhr.status === 400) {
                document.getElementById('msg').innerText = response.message;
                document.getElementById('msg').classList.add('warning');
                setTimeout(() => {
                    document.getElementById('msg').classList.add('hide');
                    setTimeout(() => {
                        document.getElementById('msg').classList.remove('warning');
                        document.getElementById('msg').classList.remove('hide');
                    }, 300);
                }, 3000);
            }

            // notifing user about server side error
            if (xhr.status === 500) {
                document.getElementById('msg').innerText = response.message;
                document.getElementById('msg').classList.add('error');
                setTimeout(() => {
                    document.getElementById('msg').classList.add('hide');
                    setTimeout(() => {
                        document.getElementById('msg').classList.remove('error');
                        document.getElementById('msg').classList.remove('hide');
                    }, 300);
                }, 3000);
            }
            file1 = response.files.booking;
            file2 = response.files.expedia;
            file3 = response.files.siteminder;
            let popup2, popup1, popup3;
            if (file1.split('.') && file1.split('.').pop() === 'xlsx') {
                popup1 = window.open(`${window.location.href}static/generatedSheet/${file1}`, '_blank');
            }
            else{
                document.getElementById('msg').innerText = file1;
                document.getElementById('msg').classList.add('error');
            }
            if (file2.split('.') && file2.split('.').pop() === 'xlsx') {
                popup2 = window.open(`${window.location.href}static/generatedSheet/${file2}`, '_blank');
            }
            else{
                document.getElementById('msg').innerText = file2;
                document.getElementById('msg').classList.add('error');
            }
            if (file3.split('.') && file3.split('.').pop() === 'xlsx') {
                popup3 = window.open(`${window.location.href}static/generatedSheet/${file3}`, '_blank');
            }
            else{
                document.getElementById('msg').innerText = file3;
                document.getElementById('msg').classList.add('error');
            }

            if (popup1 == null || typeof popup1 == 'undefined' || popup2 == null || typeof popup2 == 'undefined' || popup3 == null || typeof popup3 == 'undefined') {
                document.getElementById('msg').innerText = 'Please allow popups';
                document.getElementById('msg').classList.add('warning');
                document.getElementById('loader').classList.remove('active');
                return false;
            } else {
                window.location.reload();
            }
            return false;
        }
    }

    // sending form data to server
    xhr.open('POST', '/uploadfile/');
    xhr.send(formData);
}

const checkFileExtention = (file) => {
    const fileExtention = file.files[0].name.split('.').pop();
    if (fileExtention !== 'xlsx' && fileExtention !== 'xls' && fileExtention !== 'csv') {
        document.getElementById('msg').innerText = 'Please upload valid file';
        document.getElementById('msg').classList.add('warning');
        file.style = 'border-color: red';
        file.focus();
        setTimeout(() => {
            document.getElementById('msg').classList.add('hide');
            setTimeout(() => {
                document.getElementById('msg').classList.remove('warning');
                document.getElementById('msg').classList.remove('hide');
            }, 300);
        }, 3000);
        return false;
    } else {
        file.style = 'border-color: transparent';
    }
}

debugger;