import "./App.css";
import io from "socket.io-client";
import { useEffect, useState } from "react";
import Table from "./Components/Table";
import "./style.css";

const socket = io.connect("http://localhost:5000");
const t = [];
const m = [];
const b = [];
const v = [];

function App() {
  const [trans, setTransactions] = useState([]);
  const [miners, setMiners] = useState([]);
  const [vallets, setVallets] = useState([]);
  const [blocks, setBlocks] = useState([]);

  useEffect(() => {
    socket.emit("connectt", "Hello from react!");
  }, []);

  useEffect(() => {
    socket.on("message", (data) => {
      console.log(data);
      if (data["sender"] !== undefined) {
        setTransactions(
          trans.unshift(
            "Client " +
              data["sender"] +
              " sent " +
              data["sum"] +
              "$ to client " +
              data["reciever"] +
              ", timestamp: " +
              data["timestamp"]
          )
        );
        console.log(JSON.stringify(data));
        if (t.length >= 20) t.pop();
        t.unshift(
          "Client " +
            data["sender"] +
            " sent " +
            data["sum"] +
            "$ to client " +
            data["receiver"] +
            ", Timestamp: " +
            data["timestamp"]
        );
        setTransactions(t);
      } else if (data["blockMined"] !== undefined) {
        setMiners(miners.unshift("New miner connected."));
        console.log(JSON.stringify(data));
        if (m.length >= 20) m.pop();
        m.unshift("New miner connected.");
        setMiners(m);
      } else if (data["previous_hash"] !== undefined) {
        setBlocks(blocks.unshift("New block created."));
        if (b.length >= 20) b.pop();
        b.unshift(
          "New block created. Previous hash:" +
            data["previous_hash"] +
            ", Timestamp: " +
            data["timestamp"]
        );
        setBlocks(b);
      } else if (data["balance"] !== undefined) {
        setVallets(
          vallets.unshift("New vallet " + data["username"] + " connected.")
        );
        if (v.length >= 20) v.pop();
        v.unshift("New vallet " + data["username"] + " connected.");
        setVallets(v);
      }
    });
  }, [socket]);

  return (
    <div>
      <table>
        <tr>
          <th>Transactions:</th>
          <th>New miners:</th>
          <th>New vallets:</th>
          <th>Blocks:</th>
        </tr>
        <tr valign="top">
          <td>
            <Table t={trans} />
          </td>
          <td>
            <Table t={miners} />
          </td>
          <td>
            <Table t={vallets} />
          </td>
          <td>
            <Table t={blocks} />
          </td>
        </tr>
      </table>
    </div>
  );
}

export default App;
