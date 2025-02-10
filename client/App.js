import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </ul>
        </nav>
        
        <Switch>
          <Route path="/login">
            <LoginForm />
          </Route>
          <Route path="/register">
            <RegistrationForm />
          </Route>
          <Route path="/">
            <h1>Welcome to the User Management System</h1>
            <p>Please choose an option from above.</p>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
