import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 5; 

class QuizView extends Component {
  constructor(props){
    super();
    this.state = {
        quizCategory: null,
        previousQuestions: [], 
        showAnswer: false,
        categories: {},
        numCorrect: 0,
        currentQuestion: {},
        guess: '',
        forceEnd: false,
        users: [],
        player: null,
        newPlayer: null,
        lastScore: null
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    });
    this.getUsers();
  }

  getUsers = () => {
      $.ajax({
          url: `/users`, //TODO: update request URL
          type: "GET",
          success: (result) => {
              this.setState({ users: result.users })
              return;
          },
          error: (error) => {
              alert('Unable to load Users. Please try your request again')
              return;
          }
      })
  }

  selectCategory = ({type, id=0}) => {
    this.setState({quizCategory: {type, id}}, this.getNextQuestion)
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  setPlayer = (event) => {
      this.setState({player: event.target.value, lastScore: event.target[event.target.selectedIndex].getAttribute('data-score')})

  }

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions]
    if(this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }

    $.ajax({
      url: '/quizzes', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault();
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [], 
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

    handleInputChange = () => {
        this.setState({
            newPlayer: this.newUser.value
        })
    }

    addUser = () => {
        $.ajax({
            url: `/users`, //TODO: update request URL
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({name: this.state.newPlayer}),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: (result) => {
                this.getUsers();
                document.getElementById("add-user").reset();
                return;
            },
            error: (error) => {
                alert('Unable to Add Category. Please try your request again')
                return;
            }
        })
    }

  renderPrePlay(){
      return (
          <div className="quiz-play-holder">
              <div className="category-section">
                  <div className="choose-header">Choose Category</div>
                  <div className="category-holder">
                      <label for="all" className="select-category"> <input type="radio" id="all" name="play-category" className="play-category" onClick={this.selectCategory} />ALL</label>
                      {Object.keys(this.state.categories).map(id => {
                      return (
                        <div>
                            <label for={id} className="select-category">
                            <input type="radio"
                                   name="play-category"
                                   key={id}
                                   value={id}
                                   id={id}
                                   className="play-category"
                                   onClick={() => this.selectCategory({type:this.state.categories[id], id})} />
                                {this.state.categories[id]}
                            </label>
                        </div>
                      )
                    })}
                  </div>
              </div>
              <div className="user-section">
                  <h4>Select User to continue</h4>
                  <h3>{this.state.lastScore ? 'Last Score :' + this.state.lastScore : ''}</h3>

                  <select name="users" className="users" onChange={this.setPlayer}>
                      <option value="" key=""> Select User </option>
                      {this.state.users.map(res => {
                          return(
                              <option value={res.id} key={res.id} data-score={res.score}> {res.name} </option>
                          )
                      })}
                  </select>

                  <br />
                  <form onSubmit={this.addUser} id="add-user" className="add-user">
                      <h4>Add User?</h4>
                      <input
                          placeholder="Add User"
                          ref={input => this.newUser = input}
                          onChange={this.handleInputChange}
                      />
                      <input type="submit" value="Add" className="add-user-btn"/>
                  </form>

              </div>
          </div>
      )
  }

  submitScore = () => {
      $.ajax({
          url: `/users`, //TODO: update request URL
          type: "PATCH",
          dataType: 'json',
          contentType: 'application/json',
          data: JSON.stringify({id: this.state.player, score: this.state.numCorrect}),
          xhrFields: {
              withCredentials: true
          },
          crossDomain: true,
          success: (result) => {

              return;
          },
          error: (error) => {
              alert('Unable to Save User Score. Please try your request again')
              return;
          }
      })
  }

  renderFinalScore(){
      this.submitScore();
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
    )
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ');
    return answerArray.includes(formatGuess)
  }

  renderCorrectAnswer(){
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    return(
      <div className="quiz-play-holder">
        <div className="quiz-question">{this.state.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
        <div className="next-question button" onClick={this.getNextQuestion}> Next Question </div>
      </div>
    )
  }

  renderPlay(){
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer 
        ? this.renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div className="quiz-question">{this.state.currentQuestion.question}</div>
            <form onSubmit={this.submitGuess}>
              <input type="text" name="guess" onChange={this.handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
  }


  render() {
    return this.state.quizCategory && this.state.player
        ? this.renderPlay()
        : this.renderPrePlay()
  }
}

export default QuizView;
