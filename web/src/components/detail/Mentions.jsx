import { useState, useEffect } from 'react';
import {Header} from "semantic-ui-react";
import './Mentions.scss';
import API from "../../api";

function Mentions({ listingID }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
    }, [listingID]);

    const fetchData = () => {
        setLoading(true);
        API.get(`/api/listings/${listingID}/mentions`).then((res) => {
            setData(res.data.data);
        }).catch((e) => {
            setData([]);
        }).finally(() => setLoading(false));
    };

    return <div className="Mentions">
        <Header as="h3"> Mentions </Header>
    </div>
}

export default Mentions;