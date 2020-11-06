import React from 'react';
import { Search } from "semantic-ui-react";

import './StockSearch.css';
import API from '../api';
import stockMarketImage from '../static/stock-market.png';

function StockSearch() {
  return (
    <div className="App">
      <SearchStandard/>
    </div>
  );
}

export default StockSearch;


// TODO: try React hooks!
class SearchStandard extends React.Component {
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