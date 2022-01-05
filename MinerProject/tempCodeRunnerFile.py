transaction=Transaction.Transaction(sum,Socket(8500,'localhost'),Socket(8600,'localhost'),22222,time.time())
    print(transaction.toJSON())
    miner=Miner()