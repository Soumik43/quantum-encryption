import axios from "axios";
import "./App.css";
import { useState } from "react";
function App() {
  const [u, setU] = useState([]);
  const [v, setV] = useState([]);
  const [dectext, setDectext] = useState("");
  const [bin, setBin] = useState("");
  const handlesubmit = async (e) => {
    e.preventDefault();
    await axios
      .post("http://127.0.0.1:5000/lwe", {
        body: e.target.elements[0].value,
      })
      .then((res) => {
        console.log(res.data.data);
        setU(res.data.data["u"]);
        setV(res.data.data["v"]);
      });
  };
  const handleDecryption = async (e) => {
    e.preventDefault();
    await axios
      .post("http://127.0.0.1:5000/lwe-decrypt", {
        u: u,
        v: v,
        s: parseInt(e.target.elements[0].value),
        q: parseInt(e.target.elements[1].value),
      })
      .then((res) => {
        setDectext(res.data["string"]);
        setBin(res.data["binary"]);
      });
  };
  return (
    <div className="App">
      <header className="App-header">
        <p className="f-20 s">
          QUANTUM IMMUNE ENCRYPTION ALGORITHM USING <br></br>LEARNING WITH
          ERRORS
        </p>
        <form onSubmit={handlesubmit}>
          <label>ENTER TEXT TO BE ENCRYPTED</label>
          <br></br>
          <br></br>
          <textarea className="in" type="text"></textarea>
          <br></br>
          <input className="btn" value="ENCRYPT" type="submit"></input>
        </form>
        <br />

        {u.length === 0 ? (
          <p></p>
        ) : (
          <div className="mb">
            <h2>Ciphertext (u,v)</h2>
            <div className="flex-col">
              <div className="mr-10 matrix">
                Values of U
                <br />
                <br />
                {u.map((data, key) => {
                  return (
                    <div key={key} className="flex-row matrix-row">
                      {/* <p>[&nbsp;</p> */}
                      {data.map((num, key) => {
                        return (
                          <span key={key} className="flex-row matrix-cell">
                            <p>{num}&nbsp;</p>
                          </span>
                        );
                      })}
                      {/* <p>]</p> */}
                    </div>
                  );
                })}
              </div>
              <div>
                Values of V
                <br />
                <br />
                {v.map((data, key) => {
                  return (
                    <div key={key} className="flex-row matrix-row">
                      {/* <p>[&nbsp;</p> */}
                      {data.map((num, key) => {
                        return (
                          <span key={key} className="flex-row matrix-cell">
                            <p>{num}&nbsp;</p>
                          </span>
                        );
                      })}
                      {/* <p>]</p> */}
                    </div>
                  );
                })}
              </div>
            </div>
            <br />
            <br />
            <form onSubmit={handleDecryption}>
              <input
                type="password"
                className="in"
                placeholder="Enter Secret Key"
              ></input>
              <br></br>
              <input
                type="password"
                className="in"
                placeholder="Enter value of Q"
              ></input>
              <br />
              <input type="submit" className="btn" value="DECRYPT"></input>
            </form>
            <h2>Fromula for Decryption</h2>
            <h5>DECRYPTED_BIT=V-S*U MOD Q</h5>
            {dectext === "" ? (
              <p></p>
            ) : (
              <p>
                Decrypted text
                <br />
                <h3 className="binrep">
                  STRING REPRESENTATION
                  <br />
                  {dectext}
                </h3>
                <div className="w-50">
                  <h3 className="binrep">
                    <br />
                    BINARY REPRESENTATION <br />
                    {bin}
                  </h3>
                </div>
              </p>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
