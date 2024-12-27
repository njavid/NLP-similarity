

import React, { useState, useEffect } from "react";
import NotificationAlert from "react-notification-alert";
// react-bootstrap components
import {
  Badge,
  Button,
  Card,
  Form,
  Navbar,
  Nav,
  Container,
  Row,
  FormGroup,
  Col,
  Table,
  Alert
} from "react-bootstrap";

const SimilarityForm = () => {
  const sentenceList = [
    "غروب آفتاب در کویر چشم‌اندازی بی‌نظیر ارائه می‌دهد.",
    "دومین برد پیاپی ایران در جام جهانی فوتبال هفت نفره اتفاق افتاد",
    "نان و عسل و پنیر صبحانه کاملی به حساب می‌آید"
  ];
  const [stringsArray, setStringsArray] = useState([]); // Array of strings
  const [currentString, setCurrentString] = useState(""); // Input for new string

  const [suggestions, setSuggestions] = useState(sentenceList);
  const [loading, setLoading] = useState(false);
  const [dataset, setDataset] = useState('');
  const [querySentence, setQuerySentence] = useState('');
  const [kValue, setKValue] = useState(1);
  const [model, setmodel] = useState(1);
  const [resultData, setResult] = useState(null);
  const [alert, setAlert] = useState({ show: false, message: '', variant: '' });
  const notificationAlertRef = React.useRef(null);

  // Add string to the array
  const addString = () => {
    if (currentString.trim() !== "") {
      setStringsArray([...stringsArray, currentString.trim()]);
      setCurrentString(""); // Clear input
    }
  };

  // Remove string from the array
  const removeString = (index) => {
    const updatedArray = stringsArray.filter((_, i) => i !== index);
    setStringsArray(updatedArray);
  };
   
  const handleInputChange = (e) => {
    const input = e.target.value;
    setQuerySentence(input);

    // Filter the sentence list to show suggestions based on input
    if (input) {
      const filteredSuggestions = sentenceList.filter((sentence) =>
        sentence.toLowerCase().includes(input.toLowerCase())
      );
      setSuggestions(filteredSuggestions);
    } else {
      setSuggestions(sentenceList);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuerySentence(suggestion);
    setSuggestions([]); // Clear suggestions after selection
  };

  const notify = (place) => {
    var type = "danger";
    var options = {};
    options = {
      place: place,
      message: (
        <div>
          <div>
          There was an error processing the data.
          </div>
        </div>
      ),
      type: type,
      icon: "nc-icon nc-bell-55",
      autoDismiss: 7,
    };
    notificationAlertRef.current.notificationAlert(options);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    console.log("hello0");
    
    // Simulate posting data (replace with actual API call)
    const response = await fetch('http://127.0.0.1:8083/find-similar-sentences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stringsArray, querySentence, kValue, }),
    });
    const resultData = await response.json();
    console.log("hiiiiii2");
    console.log(resultData);

    if (!Array.isArray(resultData)) {
      notify("tc");
      console.log("show error : ");
      console.log(resultData.error);
      // setAlert({
      //   show: true,
      //   message: resultData.error,
      //   variant: 'danger'
      // });
    } else {
      setResult(resultData);
      // Optionally clear any previous alerts
      setAlert({ show: false, message: '', variant: '' });
    }
    setLoading(false);
    
  };


// const handleSubmit = async (e) => {
//   e.preventDefault();
//   const response = await fetch('http://http://127.0.0.1:8001/find-similar-sentences', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ dataset, querySentence, kValue }),
//   });
//   const data = await response.json();
//   console.log(data); // Use data to render results
// };

  return (
    <>
    <div className="rna-container">
        <NotificationAlert ref={notificationAlertRef} />
      </div>
      <Container fluid>
        <Row>
          <Col md="4">
          <Card className="card-stats">
              <Card.Header>
                <Card.Title as="h4">Set Up Query</Card.Title>
                <p className="card-category">set query parameters & configuration </p>
              </Card.Header>
              <hr></hr>
              <Card.Body>
            <Form onSubmit={handleSubmit}>

      {/* <FormGroup row>
        <Form.Label for="data" sm={10}>Sentences (As list of texts):</Form.Label><br></br>
        
          <Form.Control type="text" placeholder="Enter sentences as json"
            name="data"
            id="data"
            // value={querySentence}
            // onChange={handleInputChange}
            // value={querySentence}
            // onChange={(e) => setQuerySentence(e.target.value)}
          />
      </FormGroup> */}
      <div>
      <label>
          Add String:
          <input
            type="text"
            value={currentString}
            onChange={(e) => setCurrentString(e.target.value)}
          />
        </label>
        <button type="button" onClick={addString}>
          Add
        </button>
      </div>

      <ul>
        {stringsArray.map((string, index) => (
          <li key={index}>
            {string}{" "}
            <button type="button" onClick={() => removeString(index)}>
              Remove
            </button>
          </li>
        ))}
      </ul>


      <FormGroup row><br></br>
      <Form.Label for="querySentence" sm={2}>Query Sentence</Form.Label><br></br>
        {/* <Col sm={10}> */}
          <Form.Control type="text" placeholder="Enter sentence"
            name="querySentence"
            id="querySentence"
            value={querySentence}
            onChange={handleInputChange}
            // value={querySentence}
            // onChange={(e) => setQuerySentence(e.target.value)}
          />
        {/* </Col> */}
         {/* Display suggestions */}
      {suggestions.length > 0 && (
        <ul style={{ border: '1px solid #ccc', marginTop: '5px', padding: '5px', listStyleType: 'none', direction: 'rtl', fontSize: '10px'  }}>
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              style={{ cursor: 'pointer', padding: '5px' }}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
      </FormGroup>
      <FormGroup row><br></br>
        <Form.Label for="kValue" sm={2}>K Value</Form.Label><br></br>
        {/* <Col sm={10}> */}
        <Form.Control
            type="number"
            placeholder="Enter k"
            name="kValue"
            id="kValue"
            // value={kValue}
            onChange={(e) => setKValue(Number(e.target.value))}
          />
        {/* </Col> */}
      </FormGroup> <br></br>
      <FormGroup row><br></br>
        <Form.Label for="model" sm={2}> select model </Form.Label><br></br>
        
        <Form.Select aria-label="Default select example" onChange={(e) => setmodel(e.target.value)}>
          <option value="0">All models</option>
          <option value="1">paraphrase_multilingual_mpnet</option>
          <option value="2">paraphrase_multilingual_MiniLM</option>
          <option value="3">bert_fa_base_uncased_wikitriplet</option>
        </Form.Select>
        {/* </Col> */}
      </FormGroup> <br></br>
      <div className="text-center">
      <Button className="my-3" type="submit" color="primary" disabled={loading}>Submit</Button> 
      </div>
    </Form>
    </Card.Body>
    </Card>
          </Col>
          <Col md="8">
           {/* Show alert if needed */}
           {/* {alert.show && (
                <Alert variant="danger">
                <button
                  aria-hidden={true}
                  className="close"
                  data-dismiss="alert"
                  type="button"
                >
                  <i className="nc-icon nc-simple-remove"></i>
                </button>
                <span>
                  <b>Danger -</b>
                  This is a regular notification made with ".alert-danger"
                </span>
              </Alert>
              )} */}
          <Card className="card-stats">
              <Card.Header>
                <Card.Title as="h4" className="text-center">Similar Sentenses</Card.Title>
                {/* <p className="card-category">set query parameters & configuration </p> */}
              </Card.Header>
              {/* <hr></hr> */}
              <Card.Body>
              {resultData ? (
                    <Table>
                    <tbody>
                    <tr key={0}>
                        <td>
                        <strong>Score</strong>  
                        </td>
                        <td className="text-center">
                        <strong>Sentence</strong> 
                        </td>
                      </tr>  
                  {resultData.map(({ id, sentence, score }) => (
                
                      <tr key={id}>
                        <td>
                         {score}  
                        </td>
                        <td className="text-center" dir="rtl">
                        {sentence}
                        </td>
                      </tr>  
                   
                  ))}
                  </tbody>
                  </Table>
                ) : (
                  <p>No result yet</p>
                )}
                </Card.Body>
              </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default SimilarityForm;
