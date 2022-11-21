import React from 'react';
import {TodoTable} from './TodoComponents';
import {NotificationTable} from './NotificationComponents';

function compare(a, b) {
    return (a.id > b.id)? 1 : (a.id < b.id)? -1 : 0;
}

class App extends React.Component {
    constructor(props) {
        super(props);
        if(process.env.TODO_ENDPOINT1) {
            this.todo_endpoint1 = process.env.TODO_ENDPOINT1;
        } else {
            this.todo_endpoint1 = 'http://localhost:8000/todo/';
        }
        if(process.env.TODO_ENDPOINT2) {
            this.todo_endpoint2 = process.env.TODO_ENDPOINT2;
        } else {
            this.todo_endpoint2 = 'http://localhost:8000/todo/';
        }
        if(process.env.TODO_ENDPOINT3) {
            this.todo_endpoint3 = process.env.TODO_ENDPOINT3;
        } else {
            this.todo_endpoint3 = 'http://localhost:8000/todo/';
        }
        console.log('Using TODO endpoint at: ' + this.todo_endpoint);
        this.state = {
            opened: false,
            title: '',
            detail: '',
            completed: false,
            todos: []
        };
        this.toggleBox = this.toggleBox.bind(this);
        this.handleAdd = this.handleAdd.bind(this);
        this.handleSubmit1 = this.handleSubmit1.bind(this);
        this.handleSubmit2 = this.handleSubmit2.bind(this);
        this.handleSubmit3 = this.handleSubmit3.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    toggleBox() {
        const { opened } = this.state;
        this.setState({
            opened: !opened,
        });
    }

    handleAdd(event) {
        // reset state
        this.title = '';
        this.detail = '';
        this.toggleBox();
        event.preventDefault();
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit1(event) {
        var now = new Date();
        now.setSeconds(now.getSeconds() + 5);
        const todo = {
            title: this.state.title+" 1",
            detail: this.state.detail,
            duedate: now,
            tags: [],
            completed: this.state.completed
        }
        console.log('submit', todo);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todo)
        };
        fetch(this.todo_endpoint1, requestOptions)
            .then(response => response.json())
            .then(data => this.refresh())
            .catch(console.log);
        this.toggleBox();
        event.preventDefault();
    }

    handleSubmit2(event) {
        var now = new Date();
        now.setSeconds(now.getSeconds() + 5);
        const todo = {
            title: this.state.title+" 2",
            detail: this.state.detail,
            duedate: now,
            tags: [],
            completed: this.state.completed
        }
        console.log('submit', todo);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todo)
        };
        fetch(this.todo_endpoint2, requestOptions)
            .then(response => response.json())
            .then(data => this.refresh())
            .catch(console.log);
        this.toggleBox();
        event.preventDefault();
    }

    handleSubmit3(event) {
        var now = new Date();
        now.setSeconds(now.getSeconds() + 5);
        const todo = {
            title: this.state.title+" 3",
            detail: this.state.detail,
            duedate: now,
            tags: [],
            completed: this.state.completed
        }
        console.log('submit', todo);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todo)
        };
        fetch(this.todo_endpoint3, requestOptions)
            .then(response => response.json())
            .then(data => this.refresh())
            .catch(console.log);
        this.toggleBox();
        event.preventDefault();
    }

    refresh() {
        fetch(this.todo_endpoint1, { mode: 'cors' })
            .then(res => res.json())
            .then((data) => {
                data.sort(compare);
                this.setState( { todos: data } );
            })
            .catch(console.log);
    }

    componentDidMount() {
        this.refresh();
    }

    render() {
      const { opened } = this.state;
      return (
          <div className="App">
              <h1>
                  Uber To Do
              </h1>
              <div>
                  <NotificationTable></NotificationTable>
              </div>
              <hr />
              {!opened && (
                  <div>
                      <TodoTable todos={this.state.todos}/>
                      <hr/>
                      <input type="button" value="Add" onClick={this.handleAdd} />
                  </div>
              )}
              {opened && (
                  <div>
                      <form>
                          <label>
                              Title:
                              <input
                                  name="title"
                                  type="text"
                                  value={this.state.title}
                                  onChange={this.handleInputChange} />
                          </label>
                          <br /><br />
                          <label>
                              Detail:
                              <input
                                  name="detail"
                                  type="text"
                                  value={this.state.detail}
                                  onChange={this.handleInputChange} />
                          </label>
                          <br /><br />
                          <label>
                              Completed:
                              <input
                                  name="completed"
                                  type="checkbox"
                                  checked={this.state.completed}
                                  onChange={this.handleInputChange} />
                          </label>
                          <br /><br />
                          <input type="submit" value="Add 1" onClick={this.handleSubmit1}/>
                          <input type="submit" value="Add 2" onClick={this.handleSubmit2}/>
                          <input type="submit" value="Add 3" onClick={this.handleSubmit3}/>
                          <input type="button" value="Cancel" onClick={this.toggleBox} />
                      </form>
                  </div>
              )}
          </div>
      );
  }
}

export default App;
