import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route, Switch, useParams } from 'react-router-dom';
import './index.css';
import StockSearch from './search/StockSearch';
import Admin from './admin/Admin';
import reportWebVitals from './reportWebVitals';
import 'semantic-ui-css/semantic.min.css';

ReactDOM.render(
    <BrowserRouter>
        <Switch>
            <Route exact path="/admin" component={Admin}/>
            <Route path="/">
                <StockSearch/>
                <Switch>
                    <Route path={"/listing/:id"}>
                        <Child/>
                    </Route>
                </Switch>
            </Route>
        </Switch>
    </BrowserRouter>,
    document.getElementById('root')
);

function Child() {
    // We can use the `useParams` hook here to access
    // the dynamic pieces of the URL.
    let { id } = useParams();

    return (
        <div>
            <h3>ID: {id}</h3>
        </div>
    );
}

// If you want to start measuring performance in your search, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
