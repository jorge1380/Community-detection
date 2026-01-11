import React from 'react';

const CommunityResults = ({ results }) => {
  if (!results) return null;

  return (
    <section>
      {results.communities.length === 0 ? (
        <p>No se detectaron comunidades.</p>
      ) : (
        
      <p>Comunidades activas: {results.communities.length}</p>
      )}
    </section>
  );
};

export default CommunityResults;
