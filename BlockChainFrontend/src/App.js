import "./App.css";
import io from "socket.io-client";
import { useEffect, useState } from "react";

const socket = io.connect("http://localhost:5000");

function App() {
  useEffect(() => {
    socket.emit("connectt", "aaaa");
  }, []);
  const [poruka, setPoruka] = useState("");
  useEffect(() => {
    socket.on("message", (data) => {
      setPoruka(data);
    });
  }, [socket]);
  return <div>{poruka}</div>;
}

export default App;
