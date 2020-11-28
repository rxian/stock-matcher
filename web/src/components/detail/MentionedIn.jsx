import { useState, useEffect } from 'react';
import {Header} from "semantic-ui-react";
import './MentionedIn.scss';
import API from "../../api";

function MentionedIn({ listingID }) {
    const [newsData, setNewsData] = useState([]);

    useEffect(() => {
        API.get(`/api/news/${listingID}`).then((res) => {
            setNewsData(res.data.data);
        }).catch((e) => {
            setNewsData([]);
        });
    }, [listingID]);

    return <div className="MentionedIn">
        <div className='header-bar'> <Header as="h3"> Mentioned In </Header> </div>
        { newsData.map((item, i) =>
            <div className="list-row">
                <a href={item.url}>
                    <div className="date">{item.date}</div>
                    <div className="news-title">{item.title}</div>
                </a>
            </div>
        )}
    </div>
}

export default MentionedIn;