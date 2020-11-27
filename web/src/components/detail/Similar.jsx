import {useEffect, useState} from "react";
import API from "../../api";
import {Checkbox, Header, Loader } from "semantic-ui-react";
import ListingSummaryCard from "../listingSummary/ListingSummaryCard";
import './Similar.scss';

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
        fetchData();
    };

    useEffect(() => {
        fetchData();
    }, [listingID, startDate, endDate]);

    const customCardContent = (title, companyName, score ) =>
        <div>
            { title && <div className='title'>{title}</div> }
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
                                content={customCardContent(item.symbol, item.name, item.distance)}
            />);

    return (
        <div className="Similar">
            <div className="header-bar">
                <Header>
                    Similar Trends
                </Header>
                <Checkbox label='DTW' onChange={handleOnChange}/>
            </div>
            { loading? <Loader active/>: content }
        </div>
    );
}

export default Similar;