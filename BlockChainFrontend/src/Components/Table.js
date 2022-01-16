import io from "socket.io-client";
import { useEffect, useState } from "react";

const Table = (props) => {
  return (
    <div>
      <table>
        {Object.keys(props.t).map((key, index) => (
          <tr key={index}>{props.t[key]}</tr>
        ))}
      </table>
    </div>
  );
};

export default Table;
