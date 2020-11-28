import React from 'react';
import {Search} from "semantic-ui-react";
import './StockSearch.scss';
import API from '../../api';
import {Link} from "react-router-dom";
import ListingSummaryCard from "../listingSummary/ListingSummaryCard";
import {defaultEndDate, defaultStartDate} from "../../static/hardCodeConfig";

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
        if (data.value === "") return;

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

    resultRenderer = (item) =>
        <Link to={`/listing/${item.listing_id}`}>
            <ListingSummaryCard
                description={item.description}
                title={item.title}
                listingID={item.listing_id}
                startDate={defaultStartDate}
                endDate={defaultEndDate}
                strokeColor={"steelblue"}
                strokeWidth={"1.2"}
            />
        </Link>;

    render() {
        const { loading, results } = this.state;
        return (
            <Search
                loading={loading}
                resultRenderer={this.resultRenderer}
                onSearchChange={this.handleSearchChange}
                results={results.map((d) => ({
                    key: d['listingID'],
                    listing_id: d['listingID'],
                    title: d['symbol'],
                    description: d['name'],
                }))}
            />
        )
    }
}

export default StockSearch;
