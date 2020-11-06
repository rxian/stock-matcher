import React from 'react';
import { Search } from "semantic-ui-react";

import './StockSearch.scss';
import API from '../api';
import stockMarketImage from '../static/stock-market.png';


// TODO: try React hooks!
class StockSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            results: [],
        };

        this.handleSearchChange.bind(this);
    }

    handleSearchChange = (e, data) => {
        this.setState({ loading: true });

        API.get('/api/listings', {
            params: {
                keyword: data.value,
            }
        }).then(res => {
                this.setState({
                    loading: false,
                    results: res.data['data'],
                })
            });
    };

    render() {
        const { loading, results } = this.state;

        const data = processResult(results)
        return (
            <Search
                loading={loading}
                // onResultSelect={(e, data) => this.handleSearchChange(data)}
                // open
                onSearchChange={this.handleSearchChange}
                results={data}
            />
        )
    }
}

function processResult(data) {
    return data.map((d) => {
        return {
            title: d['symbol'],
            image: stockMarketImage
        }
    });
}

export default StockSearch;
