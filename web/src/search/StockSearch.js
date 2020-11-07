import React from 'react';
import {Search, SearchResult} from "semantic-ui-react";

import './StockSearch.scss';
import API from '../api';
import stockMarketImage from '../static/stock-market.png';
import {Link} from "react-router-dom";


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
        }).catch((e) => {
            console.log(e);
            if (e.response.status === 404) {
                this.setState({
                    results: [],
                    loading: false
                })
            }
        })
    };

    render() {
        const { loading, results } = this.state;

        const data = processResult(results)
        return (
            <Search
                loading={loading}
                onResultSelect={(e, data) => console.log(data)}
                resultRenderer={(item) => <SearchResult
                    title={item.title}
                    image={item.image}
                    description={item.name}
                    as={Link}
                    to={`/listing/${item.listing_id}`}
                />}
                onSearchChange={this.handleSearchChange}
                results={data}
            />
        )
    }
}

function processResult(data) {
    return data.map((d) => {
        return {
            key: d['listingID'],
            listing_id: d['listingID'],
            title: d['symbol'],
            description: d['name'],
            image: stockMarketImage
        }
    });
}

export default StockSearch;
