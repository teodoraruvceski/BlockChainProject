import React,{useState,useEffect} from 'react'
function App() {
  const [data,setData]=useState([{}])
  useEffect(()=>{
    fetch("\ transactions").then(
      res=>res.json()
    ).then(
      data=>{setData(data)
      console.log(data)}
    )
  })
  return (
    <div>
      {(typeof data.transactions === 'undefined')? (
        <p>Loading...</p>
      ):
      (
        data.transactions.map((transaction,i)=>(
          <p key={i}>suma: {transaction.sum}</p>
        ))
        // <p>{data.sum}</p>
        // <p>{data.sender}</p>
        // <p>{data.receiver}</p>
        // <p>{data.balance}</p>
        // <p>{data.timestamp}</p>
        // 'sum':self.sum,
        //     'sender':self.sender.dump(),
        //     'receiver':self.receiver.dump(),
        //     'balance':self.balance,
        //     'timestamp':self.timestamp
      )}
    </div>
  )
}

export default App

