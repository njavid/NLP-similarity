

import React, { useState, useEffect } from "react";

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
} from "react-bootstrap";

const SimilarityForm = () => {
  const [dataset, setDataset] = useState('');
  const [querySentence, setQuerySentence] = useState('');
  const [kValue, setKValue] = useState(1);
  const [resultData, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log("hello0");
    
    // Simulate posting data (replace with actual API call)
    const response = await fetch('http://127.0.0.1:8000/find-similar-sentences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset, querySentence, kValue }),
    });
    const resultData = await response.json();
    console.log("hiiiiii2");
    console.log(resultData);

    setResult(resultData);
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
      <Container fluid>
        <Row>
          <Col md="6">
          <Card className="card-stats">
              <Card.Header>
                <Card.Title as="h4">Set Up Query</Card.Title>
                <p className="card-category">set query parameters & configuration </p>
              </Card.Header>
              <hr></hr>
              <Card.Body>
            <Form onSubmit={handleSubmit}>
      <FormGroup row>
        <Form.Label for="model" sm={8}>Dataset</Form.Label><br></br>
        {/* <Col sm={10}> */}
          <Form.Select
            type="select"
            name="model"
            id="model"
            // value={dataset}
            onChange={(e) => setDataset(e.target.value)}
          >
            <option value="">Select a dataset</option>
            <option value="model1">model 1</option>
            <option value="model2">model 2</option>
          </Form.Select>
        {/* </Col> */}
      </FormGroup>
      <FormGroup row><br></br>
      <FormGroup row>
        <Form.Label for="dataset" sm={8}>Dataset</Form.Label><br></br>
        {/* <Col sm={10}> */}
          <Form.Select
            type="select"
            name="dataset"
            id="dataset"
            // value={dataset}
            onChange={(e) => setDataset(e.target.value)}
          >
            <option value="">Select a dataset</option>
            <option value="dataset1">Dataset 1</option>
            <option value="dataset2">Dataset 2</option>
          </Form.Select>
        {/* </Col> */}
      </FormGroup>
      <Form.Label for="querySentence" sm={2}>Query Sentence</Form.Label><br></br>
        {/* <Col sm={10}> */}
          <Form.Control type="text" placeholder="Enter sentence"
            name="querySentence"
            id="querySentence"
            // value={querySentence}
            onChange={(e) => setQuerySentence(e.target.value)}
          />
        {/* </Col> */}
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
      <div className="text-center">
      <Button className="my-3" type="submit" color="primary">Submit</Button> 
      </div>
    </Form>
    </Card.Body>
    </Card>
          </Col>
          <Col md="6">
          <Card className="card-stats">
              <Card.Header>
                <Card.Title as="h4">Similar Sentenses</Card.Title>
                {/* <p className="card-category">set query parameters & configuration </p> */}
              </Card.Header>
              {/* <hr></hr> */}
              <Card.Body>
              {resultData ? (
                    <Table>
                    <tbody>
                    <tr key={0}>
                        <td>
                        <strong>Sentence</strong>  
                        </td>
                        <td>
                        <strong>Score</strong> 
                        </td>
                      </tr>  
                  {resultData.map(({ id, sentence, score }) => (
                
                      <tr key={id}>
                        <td>
                         {sentence}  
                        </td>
                        <td className="text-center">
                        {score}
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
