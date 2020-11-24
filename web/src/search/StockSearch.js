import React, { useState, useEffect } from 'react';
import {Search} from "semantic-ui-react";
import './StockSearch.scss';
import API from '../api';
import {Link} from "react-router-dom";
import LineChart from "../chart/Chart";

const startDate = "2013-02-08";
const endDate = "2013-02-22";

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

    resultRenderer = (item) => <CustomSearchResult
        description={item.description}
        title={item.title}
        listingID={item.listing_id}
    />;

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

function CustomSearchResult({ title, description, listingID }) {
    const [data, setData] = useState([]);

    useEffect(() => {
        let isMounted = true; // NOTE: isMounted variable is used to avoid warnings when using React hook with async function.
        API.get(`/api/listings/${listingID}/prices`, {
            params: {
                "start-date": startDate,
                "end-date": endDate,
            }
        }).then((res) => {
            if (!isMounted) return;
            setData(res.data.data);
        }).catch((e) => {
            // console.log(e.response);
        });
        return () => { isMounted = false };
    }, [listingID]);

    return (
        <Link to={`/listing/${listingID}`}>
            <div key='image' className='image'>
                {data.length === 0? null:
                    <LineChart
                        data={data.map(item => ({
                            x: new Date(item.date),
                            y: item.open,
                        }))}
                        height={42}
                        width={70}/>
                }
            </div>
            <div key='content' className='content'>
                {title && <div className='title'>{title}</div>}
                {description && <div className='description'>{description}</div>}
            </div>
        </Link>
    );
}

export default StockSearch;
