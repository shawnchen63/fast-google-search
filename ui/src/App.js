import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';
import {Link} from 'react-router-dom'

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        search_query: '',
      },
      pos_result: {
        rate: '',
        title: '',
        link: ''
      },
      neu_result: {
        rate: '',
        title: '',
        link: ''
      },
      neg_result: {
        rate: '',
        title: '',
        link: ''
      }
    };
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  }

  handlePredictClick = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    fetch('http://127.0.0.1:5000/prediction/', 
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          pos_result: response.pos_result,
          neu_result: response.neu_result,
          neg_result: response.neg_result,
          isLoading: false
        });
      });
  }

  handleCancelClick = (event) => {
    this.setState({ pos_result: {
      rate: '',
      title: '',
      link: ''
      }
    });
  }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const pos_result = this.state.pos_result;
    const neu_result = this.state.neu_result;
    const neg_result = this.state.neg_result;

    return (
      <Container>
        <div>
          <h1 className="title">Fast Google Summary</h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Ask Google if something is good or bad! </Form.Label>
                <Form.Control 
                  type="text" 
                  placeholder="Example: Is hitler a good person?" 
                  name="search_query"
                  value={formData.search_query}
                  onChange={this.handleChange} />
              </Form.Group>
            </Form.Row>
            <Row>
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  { isLoading ? 'Searching... (this takes ~30s)' : 'Search' }
                </Button>
              </Col>
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}>
                  Reset search
                </Button>
              </Col>
            </Row>
          </Form>
          {pos_result["rate"] === "" ? null :
            (<div>
              <Row>
                <Col className="result-container">
                  <h5 id="pos_result">{pos_result["rate"]}</h5>
                </Col>
                <Col className="result-container">
                  <h5 id="neu_result">{neu_result["rate"]}</h5>
                </Col>
                <Col className="result-container">
                  <h5 id="neg_result">{neg_result["rate"]}</h5>
                </Col>
              </Row>
              <Row>
                <Col className="result-container">
                  <h5 id="pos_result">Most Positive Article:</h5>
                </Col>
                <Col className="result-container">
                  <h5 id="neg_result">Most Negative Article:</h5>
                </Col>
              </Row>
              <Row>
                <Col className="title-container">
                  <a href={pos_result["link"]}>
                  <h5 id="title">{pos_result["title"]}</h5>
                  </a>
                </Col>
                <Col className="title-container">
                  <a href={neg_result["link"]}>
                  <h5 id="title">{neg_result["title"]}</h5>
                  </a>
                </Col>
              </Row>
            </div>)
          }
        </div>
      </Container>
    );
  }
}

export default App;