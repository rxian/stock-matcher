import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route, Switch } from 'react-router-dom';
import './index.scss';
import reportWebVitals from './reportWebVitals';
import 'semantic-ui-css/semantic.min.css';
import { Header } from "semantic-ui-react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import { faDog } from "@fortawesome/free-solid-svg-icons";
import StockSearch from "./components/search/StockSearch";
import Detail from "./components/detail/Detail";
import Admin from "./components/admin/Admin";

ReactDOM.render(
    <BrowserRouter>
        <Switch>
            <Route exact path="/admin" component={Admin}/>
            <Route path="/">
                <App/>
            </Route>
        </Switch>
    </BrowserRouter>,
    document.getElementById('root')
);

function App() {
    return (
        <div className="App">
            <Header as='h1'>
                <FontAwesomeIcon icon={faDog} />
                Stock Matcher
            </Header>
            <StockSearch/>
            <Switch>
                <Route path={"/listing/:id"}>
                    <Detail/>
                </Route>
            </Switch>
        </div>
    )
}

// If you want to start measuring performance in your search, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
