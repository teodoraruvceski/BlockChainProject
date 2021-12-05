response=s.recv(1024)
        print(pickle.load(response))
        if(pickle.loads(response)=='ok'):
            lock.acquire()
            vallet.setBalance((int)(vallet.getBalance())-sum)
            print('balance=',vallet.getBalance())
            input()
            lock.release()
        else:
            print('Couldnt send money. Not enough balance.')