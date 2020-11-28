import {useEffect, useState} from "react";
import API from "../../api";
import {Checkbox, Header, Loader } from "semantic-ui-react";
import ListingSummaryCard from "../listingSummary/ListingSummaryCard";
import './Similar.scss';
import {Link} from "react-router-dom";

function Similar({ listingID, startDate, endDate }) {
    const [data, setData] = useState([]);
    const [useDTW, setUseDTW] = useState(false);
    const [loading, setLoading] = useState(false);


    const fetchData = () => {
        setLoading(true);

        API
            .get(`/api/listings/${listingID}/similar`, {
                params: {
                    "start-date": startDate,
                    "end-date": endDate,
                    "dtw": useDTW,
                }
            })
            .then((res) => {
                if (useDTW) setData(res.data.data);
                else setData(res.data.data);
            })
            .catch((e) => { setData([]); })
            .finally(() => setLoading(false));
    };

    const handleOnChange = (e, data) => {
        setUseDTW(data.checked);
    };

    useEffect(() => {
        fetchData();
    }, [listingID, startDate, endDate, useDTW]);

    const customCardContent = (title, companyName, score, listingID ) =>
        <div>
            { <Link to={`/listing/${listingID}`}><div className='title'>{title}</div></Link> }
            { companyName && <div className='description'>{companyName}</div> }
            { score && <div> Score: { score.toFixed(2) }</div> }
        </div>;

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
                                strokeWidth={2}
                                content={customCardContent(item.symbol, item.name, item.distance, item.listingID)}
            />);

    return (
        <div className="Similar">
            <div className="header-bar">
                <Header as="h1">
                    Similar Trends
                </Header>
                <Checkbox label='DTW' onChange={handleOnChange}/>
            </div>
            { loading? <Loader active/>: content }
        </div>
    );
}

export default Similar;