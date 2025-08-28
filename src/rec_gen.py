from src.recommend import recommendFromGenres, fetch_poster
from src.search_movie import get_movie_details, get_movie_credits
import streamlit as st

def rec_by_genre(genre):
    rec_ids, rec_names, rec_posters = recommendFromGenres(genre)

    # Cache recommendations for consistent UI after rerun
    # if "recommendation_cache" not in st.session_state:
    #     st.session_state.recommendation_cache = recommendFromGenres(genre)

    # rec_ids, rec_names, rec_posters = st.session_state.recommendation_cache

    if not rec_names:
        st.info(f"No movies found in {genre}.")
        return  

    for idx, m_id in enumerate(rec_ids):
        details = get_movie_details(m_id)
        poster = fetch_poster(m_id)
        credits = get_movie_credits(m_id)
        
        cast = [c["name"] for c in credits.get("cast", [])[:5]]
        directors = [c["name"] for c in credits.get("crew", []) if c["job"] == "Director"]

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(poster, use_container_width=True)

        with col2:
            st.markdown(f"""
                <div style="color: white;">
                    <h3 style="margin-bottom: 0;">{details.get('title', 'Unknown Title')}</h3>
                    <p style="margin-top: 0; color: gray;">Release Date: {details.get('release_date', 'N/A')}</p>
                    <p>{details.get('overview', 'No overview available.')}</p>
                    <p><strong>Rating:</strong> {details.get('vote_average', 'N/A')} ⭐</p>
                    <p><strong>Director:</strong> {', '.join(directors) if directors else 'N/A'}</p>
                    <p><strong>Cast:</strong> {', '.join(cast) if cast else 'N/A'}</p>
                </div>
            """, unsafe_allow_html=True)

        # Optional spacing between cards
        st.markdown("---")
