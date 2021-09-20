from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .generate_key import *
from django.utils import six
from .public_key_infrastructure import *
from .models import *


# Create your views here.
def login_view(request):
    next = request.GET.get('next')
    form = LoginFormAuth(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        u = authenticate(username=username, password=password)
        login(request, u)
        if next:
            return redirect(next)
        return redirect('/')
    return render(request, 'crypto/login.html', {'form': form})


def signup(request):
    next = request.GET.get('next')
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.email, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'crypto/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def home_view(request):
    return render(request, 'crypto/home.html', {})


def about_view(request):
    return render(request, 'crypto/about.html', {})


def key(request):
    y = 0
    z = 0
    if request.method == 'POST':
        if 'gen' in request.POST:
            x = generateKey(1024)
            y = x[0]
            z = x[1]
    return render(request, 'crypto/generate.html', {'public_key': y, 'private_key': z})


@login_required
def messages_view(request):
    if request.method == 'POST':
        form = MessagesForm(request.POST)
        if 'enc' in request.POST:
            a = request.POST
            t = dict(six.iterlists(a))
            p = list(t.values())[1][0]
            w = list(t.values())[2][0]
            u = CustomeUser.objects.filter(id=int(p)).values('public_key')
            z = u[0]
            c = z.get("public_key", "")

            def readpubKeyFile():
                content2 = list(map(int, c.strip().split(',')))
                keySize, n, EorD = content2[0], content2[1], content2[2]
                return (int(keySize), int(n), int(EorD))

            def encryptAndWriteToFile(message, blockSize=None):
                keySize, n, e = readpubKeyFile()
                if blockSize == None:
                    blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
                if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
                    sys.exit(
                        'ERROR: Block size is too large for the key and symbolset size. Did you specify the correct key file and encryptedfile?')
                encryptedBlocks = encryptMessage(message, (n, e), blockSize)
                for i in range(len(encryptedBlocks)):
                    encryptedBlocks[i] = str(encryptedBlocks[i])
                encryptedContent = ','.join(encryptedBlocks)
                encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
                return encryptedContent
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.Message = encryptAndWriteToFile(w)
            message.save()
            return redirect('/')
    else:
        form = MessagesForm()
    return render(request, 'crypto/message.html', {'form': form})


@login_required
def decrypt_view(request):
    tf = ''
    mess = Messages.objects.filter(receiver=request.user)
    if request.method == 'POST':
        r = request.POST
        tw = dict(six.iterlists(r))
        em = list(tw.values())[1][0]
        pk = list(tw.values())[2][0]
        print(em)
        print(pk)

        def readpriKeyFile():
            try:
                content1 = list(map(int, pk.strip().split(',')))
                keySize, n, EorD = content1[0], content1[1], content1[2]
            except Exception as e:
                error_display = e
            return (int(keySize), int(n), int(EorD))

        def readFromFileAndDecrypt(message2):
            keySize, n, d = readpriKeyFile()
            messageLength, blockSize, encryptedMessage = message2.split('_')
            messageLength = int(messageLength)
            blockSize = int(blockSize)
            if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
                sys.exit(
                    'ERROR: Block size is too large!')
            encryptedBlocks = []
            for block in encryptedMessage.split(','):
                encryptedBlocks.append(int(block))
            return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)

        tf = readFromFileAndDecrypt(em)

    return render(request, 'crypto/decrypt.html', {"tf": tf, "mess": mess})
