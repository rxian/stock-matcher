import {useEffect, useState} from "react";
import API from "../../api";
import {Checkbox, Header, Loader } from "semantic-ui-react";
import ListingSummaryCard from "../listingSummary/ListingSummaryCard";
import './Similar.scss';

function Similar({ listingID, startDate, endDate }) {
    const [data, setData] = useState([]);
    const [useDTW, setUseDTW] = useState(false);
    const [dataDTW, setDataDTW] = useState([]);
    const [loading, setLoading] = useState(false);


    const fetchData = () => {
        setLoading(true);

        API.get(`/api/listings/${listingID}/similar`, {
            params: {
                "start-date": startDate,
                "end-date": endDate,
                "dtw": useDTW,
            }
        }).then((res) => {
            if (useDTW) {
                setData(res.data.data);
            } else {
                setData(res.data.data);
            }

            setLoading(false);
        }).catch((e) => {
            setData([]);
            setLoading(false);
        });
    };

    const handleOnChange = (e, data) => {
        setUseDTW(data.checked);
        fetchData();
    };

    useEffect(() => {
        fetchData();
    }, [listingID, startDate, endDate]);

    const content = data.length === 0? <p>No data</p>:
        data.map((item, i) =>
            <ListingSummaryCard key={i}
                                listingID={item.listingID}
                                title={item.symbol}
                                price
                                width={400}
                                height={100}
                                startDate={startDate}
                                endDate={endDate}
            />);

    return (
        <div className="Similar">
            <Header as="h3">
                Similar Trends
                <Checkbox label='DTW' onChange={handleOnChange}/>
            </Header>
            { loading? <Loader active/>: content }
        </div>
    );
}

export default Similar;